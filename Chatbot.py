from simpleaichat import AIChat
import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")

# Sidebar
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

    option = st.selectbox(
    'Elige la comunidad',
    #('comunidad-0', 'comunidad-1', 'comunidad-2', 'comunidad-4'))
    ('comunidad-C0', 'comunidad-C1', 'comunidad-C2'))

# Read dict from 'comunidad-0.txt' file
with open(f'{option}.txt', 'r') as file:
    data = file.read().replace('\n', '')
    # convert string to dict
    data = eval(data)

SYSTEM_PROMPT = f"""
                Eres {data['name']}, un cliente de un supermercado.
                Tu edad es {data['age']} años.
                Tu ocupación es {data['ocuppation']}.
                Así te describe el equipo de marketing del supermercado: {data['description']}.
                Tus dolores son: {data['pains']}.
                Tus motivaciones de compra son: {data['buying_motivations']}.
                Un ejemplo de una lista de cosas que comprarías en el supermercado son: {data['buying_list']}.
                Responde de forma amable y educada.
                """

st.title(f"{data['title']}")

# Columns with text
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Comunidad")
    st.write(f"{data['community_description']}")

with col2:
    st.header("Buyer Persona")
    st.write(f"*Nombre:* {data['name']}")
    st.write(f"*Edad:* {data['age']}")
    st.write(f"*Ocupación:* {data['ocuppation']}")
    st.write(f"*Descripción:* {data['description']}")
    st.write(f"*Dolores:* {data['pains']}")
    st.write(f"*Motivaciones de compra:* {data['buying_motivations']}")
    st.write(f"*Lista de compra de ejemplo:* {data['buying_list']}")

with col3:
    image = Image.open(f'imgs/{option}.png')
    st.image(image, caption=f"{data['name']}")

# ChatGPT interface
st.header("💬 Chatea con tu Cliente")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state["messages"] = [{"role": "assistant", "content": f"¡Hola! ¿En que te puedo ayudar?"}]

for msg in st.session_state.messages:
    if (msg['role'] == "assistant") or (msg['role'] == "user"):
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Tu mensaje"):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    ai = AIChat(system=SYSTEM_PROMPT, model="gpt-3.5-turbo", api_key = openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = ai(prompt)
    msg = {"role": "assistant", "content": response}
    #msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg["content"])