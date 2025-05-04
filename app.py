import os
import openai
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv, find_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableLambda
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.document_compressors.rankllm_rerank import RankLLMRerank
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st


_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key  = os.environ['OPENAI_API_KEY']
embedding = OpenAIEmbeddings(model = "text-embedding-3-small")
persist_directory = 'Data/Chroma/'

# Initialise Vector DB
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

# Initialise llm
openai.api_key = os.environ['OPENAI_API_KEY']
llm = ChatOpenAI(model = "gpt-4o-mini" ,temperature=0)

# Initialise reranker
compressor = RankLLMRerank(top_n=3, model="gpt", gpt_model="gpt-4o-mini")
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=vectordb.as_retriever(search_kwargs={"k": 10})
)

# Build prompt template
template = """You are an expert on the Singapore Budget 2024 who is here to help the public by answering questions from the users based on the information that has been provided below.
Only use the context provided to answer the question at the end. If you don't know the answer from the context, respond that you are unable to answer the questions outside of the context of Singapore Budget 2024. 
You can ask the user to provide more information specifically only when it can help you answer their question better.

{context}

Question: {query}

Answer:

Specify the Source of information from the "Source" keyword that is provided in the context that your answer was generated with from whenever possible. 

"""

class RelevanceResponse(BaseModel):
    response: str = Field(title="Determines if context provided is relevant", description= "Output only 'relevant' or 'irrelevant'.")
relevance_prompt = PromptTemplate(
    input_variables=["query", "context"],
    template="Given the query '{query}' and the context '{context}', determine if the context is relevant to the query. Output only 'relevant' or 'irrelevant'."
)

QA_CHAIN_PROMPT = ChatPromptTemplate.from_template(template)

# Create LLMChains for each step
# Relevance chain to be forced with a stuctured output
relevance_chain = relevance_prompt | llm.with_structured_output(RelevanceResponse)

# Streamlit outputs a different character format whenever a $ is in the string. 
def Streamlit_Output_Parse(output_str):
    return output_str.replace("$", "\$")

# Generation chain will not require a stuctured output
generation_chain = (
    RunnablePassthrough() | QA_CHAIN_PROMPT | llm | StrOutputParser() | RunnableLambda(Streamlit_Output_Parse)
)


st.title("Singapore Budget 2024 Chatbot")

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("Ask me anything about Singapore Budget 2024!")


def self_rag(query):

    # Step 1: Retrieve documents with similarity and rerank
    docs = compression_retriever.invoke(query)

    # Include the source of information for each of the context. Should update the metadata without the file path into vectordb in the future
    contexts = [doc.page_content + " Source: " + doc.metadata["source"].replace("../Data/Budget2024_Documents/", "") for doc in docs]
    print(f"Retrieved {len(contexts)} documents")
    print(contexts)

    # Step 2: Evaluate relevance of retrieved documents
    print("Step 2: Evaluating relevance of retrieved documents...")
    relevant_contexts = []
    for i, context in enumerate(contexts):
        input_data = {"query": query, "context": context}
        relevance = relevance_chain.invoke(input_data).response.strip().lower()   # Run chain
        print(f"Document {i+1} relevance: {relevance}")
        if relevance == 'relevant':
            relevant_contexts.append(context)
    print(f"Number of relevant contexts: {len(relevant_contexts)}")
        

    # Step 3a: If no relevant contexts found, direct the LLM to respond with no answer found
    if not relevant_contexts:
        print("No relevant contexts found. Generating without using any provided context")
        input_data = {"query": query, "context": "No relevant context found."}
        # response = generation_chain.invoke(input_data) # Run chain
        return generation_chain.stream(input_data)
    
    # Step 3b: Else if there are relevant context, respond using the relevant contexts provided
    else:
        print("Step 4: Generating responses with contexts...")
        print(contexts)
        input_data = {"query": query, "context": contexts}
        # response = generation_chain.invoke(input_data)  # Run chain
        return generation_chain.stream(input_data)
    
# Method to display message on the UI
def display_msg(msg, author):

    st.session_state.messages.append({"role": author, "content": msg})
    st.empty()
    st.chat_message(author).write(msg)

if prompt:
    
    display_msg(prompt, "user")

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            final_response = st.write_stream(self_rag(prompt))
            # final_response = self_rag(prompt)
            # st.write(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})
