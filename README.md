# This is a Chatbot for Budget 2024
The LangChain framework was used to implement the chatbot, and Streamlit was used as the front-end framework for the users to interact with.
A brief overview of the entire flow is as shown in the diagram below.
![Overall_Architectural_Diagram](https://github.com/user-attachments/assets/3a6773f6-4161-4175-a2a2-6a55c81a444f)

A detailed overview of the RAG flowchart is shown below.
![Flowchart](https://github.com/user-attachments/assets/5ed20f11-86e9-48ae-91a9-af6bc1dd5862)  

## Pre-requisites  
Install the necessary packages by installing Python packages via pip. You can choose to create your own virtual environment before doing so.

```bash
  pip install -r requirements.txt
  ```

Update the .env file with your own <OPEN_API_KEY>

Once the packages have been fully installed, run the following:
```bash
  streamlit run app.py
  ```
The streamlit application can now be accessed from 'localhost:8501'. 

## Run with Docker

In progress...
