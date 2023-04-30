import openai
import streamlit as st

# Configuración de OpenAI
openai.api_key = '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'# Reemplaza con tu propia API key
model_engine = "text-davinci-002" # El modelo que usaremos para generar respuestas

# Función para generar la respuesta del modelo
def generate_response(prompt):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].text
    return message.strip()

# Configuración de la página de Streamlit
st.set_page_config(page_title="ChatGPT", page_icon=":speech_balloon:")
st.title("ChatGPT")

# Configuración de la barra lateral de Streamlit
st.sidebar.title("Configuración")
user_name = st.sidebar.text_input("Nombre de usuario", value="Yo")
bot_name = st.sidebar.text_input("Nombre del bot", value="ChatGPT")

# Configuración del chat
st.write(f"Bienvenido al chat, {user_name}!")
conversation = st.empty()
message = st.text_input(f"Escribe un mensaje, {user_name}:", key="input")

if st.button("Enviar"):
    if message:
        # Generamos la respuesta del modelo y la agregamos a la conversación
        prompt = f"{user_name}: {message}\n{bot_name}: "
        response = generate_response(prompt)
        conversation.write(f"{user_name}: {message}")
        conversation.write(f"{bot_name}: {response}")
        message = ""