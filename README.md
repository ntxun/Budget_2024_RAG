# This is a Chatbot for Budget 2024
The LangChain framework was used to implement the chatbot, and Streamlit was used as the front-end framework for the users to interact with.
A brief overview of the entire flow is as shown in the diagram below.
![Overall_Architectural_Diagram](https://github.com/user-attachments/assets/3a6773f6-4161-4175-a2a2-6a55c81a444f)

A detailed overview of the RAG flowchart implemented is shown below.
![Flowchart](https://github.com/user-attachments/assets/5ed20f11-86e9-48ae-91a9-af6bc1dd5862)  

## Pre-requisites  

### Run with Anaconda 

#### You should have Anaconda Distribution installed for the following commands below. You can visit https://www.anaconda.com/download. If you are using Python instead of Anaconda, udpate the commands below accordingly.

Install the necessary packages by installing Python packages via pip. You can choose to create your own virtual environment before doing so.
To create your own virtual environment:

```bash
  conda create -n <your_env_name> python=3.12.7
  ```
Then activate your virtual environment:

```bash
  conda activate <your_env_name>
  ```
The Chroma library will require the dependency installed before you can install with pip. On Linux, run the following:

```bash
  apt-get update --fix-missing && apt-get install -y --fix-missing build-essential
  ```
For Windows, please follow the guide to install the C++ Build Tools and follow the guide here: https://github.com/bycloudai/InstallVSBuildToolsWindows

Now, install the python library requirements

```bash
  pip install -r requirements.txt
  ```
Update the .env file with your own <OPEN_API_KEY>

Once the packages have been fully installed and you have updated the .env file with your OpenAI API Key, run the following:
```bash
  streamlit run app.py
  ```
The streamlit application can now be accessed from 'localhost:8501' like this:
![App_Page](https://github.com/user-attachments/assets/9e1ad7c6-abc3-4838-bd44-a2d1b2fbf56a)


## Run with Docker
#### You should have Docker installed for the following commands below.

Locate the .env file and update with your own <OPEN_API_KEY>

In the same folder as the DockerFile provided, run the following command:
```bash
  docker build --tag rag-app .
  ```
This will take a while for the Docker Image to be built. Once the Docker image has been built run the next command to start the container:

```bash
  docker run --rm -ti -p 8501:8501 rag-app
  ```

The streamlit application can now be accessed from 'localhost:8501'
