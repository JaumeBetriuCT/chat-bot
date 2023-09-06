import os
import sys
import constants
import streamlit as st
from PIL import Image

from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI

# llm = OpenAI(openai_api_key="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")
# Personal: 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
# Connecthink: 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

os.environ["OPENAI_API_KEY"] = constants.APIKEY

st.title("DQS chatbot application")

dqs_logo = Image.open('dqs_logo.png')
st.image(dqs_logo)

query = st.text_input("👋 Hola! Estoy aqui para ayudarte. Preguntame cualquier cosa.")
#query = sys.argv[1]

loader = TextLoader("chatbot_databases/Index_chatbot.txt")
index = VectorstoreIndexCreator().from_loaders([loader])

response = index.query(query)

if response == " No sé.":
# Posible negative responses:
#   "No dispongo de la información para responder a tu pregunta"
#   "No se sabe."
    st.write("No dispongo de la información para responder a tu pregunta")
else:
    st.write(response)

