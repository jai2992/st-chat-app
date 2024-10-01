import streamlit as st
import pandas as pd
import groq
import os
import time
import numpy as np
import streamlit as st

st.title("Chat with Llama")
if "GROQ_API_KEY" not in st.secrets:
    st.error("Please create a secrets.toml file with a GROQ_API_KEY")
else:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

client = groq.Client(api_key=GROQ_API_KEY)

def stream_data(txt):
    for word in txt.split(" "):
        yield word + " "
        time.sleep(0.05)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        chat_completion = client.chat.completions.create(
            messages=st.session_state.messages,
            model="llama-3.1-70b-versatile",
        )
        response = chat_completion.choices[0].message.content
        st.write_stream(stream_data(response))
    
    st.session_state.messages.append({"role": "assistant", "content": response})
