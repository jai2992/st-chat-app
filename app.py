import streamlit as st
import pandas as pd
import groq
import time

st.set_page_config(initial_sidebar_state="collapsed")
st.title("Ask LLM Anything")

if "GROQ_API_KEY" not in st.secrets:
    st.error("Please create a secrets.toml file with a GROQ_API_KEY")
else:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

client = groq.Client(api_key=GROQ_API_KEY)

groq_models = ['llama-3.1-70b-specdec','distil-whisper-large-v3-en', 'gemma2-9b-it', 'gemma-7b-it (DEPRECATED)', 'llama-3.3-70b-versatile', 'llama-3.1-70b-versatile (DEPRECATED)', 'llama-3.1-8b-instant', 'llama-guard-3-8b', 'llama3-70b-8192', 'llama3-8b-8192', 'mixtral-8x7b-32768', 'whisper-large-v3', 'whisper-large-v3-turbo', 'llama3-groq-70b-8192-tool-use-preview', 'llama3-groq-8b-8192-tool-use-preview', 'llama-3.3-70b-specdec', 'llama-3.2-1b-preview', 'llama-3.2-3b-preview', 'llama-3.2-11b-vision-preview', 'llama-3.2-90b-vision-preview']

selected_model = st.sidebar.selectbox("Select a model", groq_models)

if "messages" not in st.session_state:
    st.session_state.messages = []

def stream_data(txt):
    for word in txt.split(" "):
        yield word + " "
        time.sleep(0.05)

prompt = st.chat_input("What is up?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    chat_completion = client.chat.completions.create(
        messages=st.session_state.messages,
        model=selected_model,
    )
    response = chat_completion.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": response})

    st.session_state.clear_input = True

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"] or ' ')