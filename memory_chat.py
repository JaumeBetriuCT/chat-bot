import os
import sys
import streamlit as st
from PIL import Image
from utils.functions import is_negative_response

from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from htmlTemplates import css, bot_template, user_template

# llm = OpenAI(openai_api_key="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")
# Personal: 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
# Connecthink: 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

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever=vectorstore,
        memory=memory
    )

    return conversation_chain


st.write(css, unsafe_allow_html=True)

if "conversation" not in st.session_state:
    st.session_state.conversation = None

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

st.title("DQS chatbot application")

dqs_logo = Image.open('images/dqs_logo.png')
gpt_logo = Image.open("images/Chat_gpt_logo.png")

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
    
    extense = st.checkbox("Genera una respuesta extensa (Comporta tiempos de carga ligeramente superiores)")
    
    #query = sys.argv[1]

    submit_button_clicked = st.form_submit_button(label="Submit")

if submit_button_clicked:
    with st.spinner("Preparando la mejor respuesta para tu pregunta..."):

        loader = TextLoader(f"chatbot_databases/{mode}_data.txt")
        index = VectorstoreIndexCreator().from_loaders([loader])

        st.session_state.conversation = get_conversation_chain(index)

        st.write(user_template.replace("{{MSG}}", "hello robot"), unsafe_allow_html=True)
        st.write(bot_template.replace("{{MSG}}", "hello human"), unsafe_allow_html=True)


        
#         if extense:
#             query = query + " Necessito que me des una respuesta extensa."

#         # query = "Contesta la siguiente petición solo si estas al 100% seguro de que es cierta. Si no estas seguro contesta que no lo sabes:" + query

#         response = index.query(query, llm=ChatOpenAI())

#         if is_negative_response(response):
#             st.warning("No dispongo de la información para responder a tu pregunta. Para una informacion más detallada visita la web https://www.dqsconsulting.com/dqsconsulting/ o contacta con nosotros rellenando el formulario https://www.dqsconsulting.com/contacto/")
#         else:
#             st.info(response)

# with st.columns(2)[1]:
#     st.write("Powered by:")
#     st.image(gpt_logo, width=250)