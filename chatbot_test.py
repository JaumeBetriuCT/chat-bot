import os
import sys
import streamlit as st
from PIL import Image

from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI

# llm = OpenAI(openai_api_key="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")
# Personal: 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
# Connecthink: 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

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

st.title("DQS chatbot application")

dqs_logo = Image.open('dqs_logo.png')
gpt_logo = Image.open("Chat_gpt_logo.png")

st.image(dqs_logo)

mode_radio = st.radio(
    "Por favor, selecciona el tema en el que necesitas que te asesore:",
    [
        "Quiero conocer DQS y explorar los servicios que ofrecen sin entrar en detalle",
        "Estoy interesado en el paquete de aplicaciones Dynamics 365",
        "Estoy interesado en conocer los servicios que ofrece DQS en el ámbito de la Inteligencia Artificial"
    ]
)

modes_dict = {
    "Quiero conocer DQS y explorar los servicios que ofrecen sin entrar en detalle": ("general", "Puedes preguntarme lo que quieras de nuestra empresa"),
    "Estoy interesado en el paquete de aplicaciones Dynamics 365": ("dynamics", "Puedes preguntarme lo que quieras sobre el paquete de aplicaciones Dynamics 365"),
    "Estoy interesado en conocer los servicios que ofrece DQS en el ámbito de la Inteligencia Artificial": ("IA", "Puedes preguntarme lo que quieras sobre servicios que ofrece DQS en el ámbito de la Inteligencia Artificial")
}

mode, text_input_label = modes_dict[mode_radio]

with st.form(key="text_input"):
    query = st.text_input(f"👋 Hola! Soy el Chat-Bot de DQS. {text_input_label}")
    #query = sys.argv[1]

    submit_button_clicked = st.form_submit_button(label="Submit")

if submit_button_clicked:

    if mode == "general":
        loader = TextLoader("chatbot_databases/Index_chatbot.txt")
        index = VectorstoreIndexCreator().from_loaders([loader])

        response = index.query(query)

        if response == " No sé.":
        # Posible negative responses:
        #   "No dispongo de la información para responder a tu pregunta"
        #   "No se sabe."
        #   "No sabemos ..."
        #    "No lo sé."
        #    Si gpt responde algo que tenga relación con la palabra "esquema" acostumbra a ser una respuesta negativa

            st.warning("No dispongo de la información para responder a tu pregunta. Para una informacion más detallada visita la web https://www.dqsconsulting.com/dqsconsulting/ o contacta con nosotros rellenando el formulario https://www.dqsconsulting.com/contacto/")
        else:
            st.info(response)

    if mode == "dynamics":
        loader = TextLoader("chatbot_databases/dynamics_data.txt")
        index = VectorstoreIndexCreator().from_loaders([loader])

        response = index.query(query)

        if response == " No sé.":
            st.warning("No dispongo de la información para responder a tu pregunta. Para una informacion más detallada visita la web https://www.dqsconsulting.com/dqsconsulting/ o contacta con nosotros rellenando el formulario https://www.dqsconsulting.com/contacto/")
        else:
            st.info(response)

    if mode == "IA":
        st.info("El chatbot entrenado con información sobre inteligencia artificial aún no esta disponible")

with st.columns(2)[1]:
    st.write("Powered by:")
    st.image(gpt_logo, width=250)

