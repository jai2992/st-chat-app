import streamlit as st
import pandas as pd
import groq
import os
import time
import numpy as np

st.title("Chat with Llama")

# Check if the GROQ API Key is available in the secrets
if "GROQ_API_KEY" not in st.secrets:
    st.error("Please create a secrets.toml file with a GROQ_API_KEY")
else:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

client = groq.Client(api_key=GROQ_API_KEY)

# List of Groq models
groq_models = [
    "distil-whisper-large-v3-en",
    "gemma2-9b-it",
    "gemma-7b-it",
    "llama3-groq-70b-8192-tool-use-preview",
    "llama3-groq-8b-8192-tool-use-preview",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "llama-guard-3-8b",
    "llava-v1.5-7b-4096-preview",
    "llama3-70b-8192",
    "llama3-8b-8192",
    "mixtral-8x7b-32768",
    "whisper-large-v3"
]

# Sidebar dropdown for selecting the model
selected_model = st.sidebar.selectbox("Select a model", groq_models)

def stream_data(txt):
    for word in txt.split(" "):
        yield word + " "
        time.sleep(0.05)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input box for user prompt
if prompt := st.chat_input("What is up?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate assistant response using the selected model
    with st.chat_message("assistant"):
        chat_completion = client.chat.completions.create(
            messages=st.session_state.messages,
            model=selected_model,  # Use the selected model from the dropdown
        )
        response = chat_completion.choices[0].message.content
        st.write_stream(stream_data(response))
    
    st.session_state.messages.append({"role": "assistant", "content": response})
