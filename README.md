# DQS consulting chatbot
This repo contains the implementation of a chatbot designed to answer questions about the services of the compant DQS consulting based in Spain. 

## Data
The data used in this project is the public data of the DQS webpage https://www.dqsconsulting.com/. To use the chatbot with your own custom data replace the file general_data.txt inside the folder chatbot_databases with your own data.

## Run the streamlit app
The project uses the library langchain for finetunning the GPT model to your own data and Streamlit for creating a user-friendly interface.

To run the aplication locally simply type into a terminal:

```
streamlit run memeory_chat.py
```

if you want to use the first version without memeory:

```
streamlit run chatbot_test.py
```

## Cloud deploy
The repo can be deployed on streamlit cloud following the instructions in the page: https://streamlit.io/cloud

Once deployed the app will be accessible from any device using a navigator.

## Open AI api-keys management
To add the Open AI key create a folder in the repo with the name .streamlit and inside crate a file named secrets.toml and add the key with the format:

OPENAI_API_KEY="sk-..."