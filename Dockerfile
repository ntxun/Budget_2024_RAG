# Use an official Anaconda image as the base image
FROM continuumio/miniconda3

# Set the working directory inside the container
WORKDIR /app

COPY . .

RUN apt-get update --fix-missing && apt-get install -y --fix-missing build-essential

# Prepare the environment
RUN conda env create --file docker_environment.yml

SHELL ["conda", "run", "--name", "rag-app", "/bin/bash", "-c"]

# Expose the port that the Python app will run on
EXPOSE 8501

# Ensure the conda environment is activated in future commands
ENV PATH="/opt/conda/envs/rag-app/bin:$PATH"

CMD ["conda", "run", "--name", "rag-app", "streamlit", "run", "app.py"]

