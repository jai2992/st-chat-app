import streamlit as st
import pandas as pd
import groq
import time

# Check if the GROQ API Key is available in the secrets
if "GROQ_API_KEY" not in st.secrets:
    st.error("Please create a secrets.toml file with a GROQ_API_KEY")
else:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

client = groq.Client(api_key=GROQ_API_KEY)

# List of Groq models
groq_models = [
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "llama-3.2-1b-preview",
    "llama-3.2-3b-preview",
    "llama-3.2-11b-vision-preview",
    "mixtral-8x7b-32768"
]

# Sidebar dropdown for selecting the model
selected_model = st.sidebar.selectbox("Select a model", groq_models)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

def stream_data(txt):
    for word in txt.split(" "):
        yield word + " "
        time.sleep(0.05)

# Input box for user prompt
prompt = st.text_input("What is up?", placeholder="Ask the AI anything...")

if prompt:
    # Add the message as a new input
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate assistant response using the selected model
    chat_completion = client.chat.completions.create(
        messages=st.session_state.messages,
        model=selected_model,  # Use the selected model from the dropdown
    )
    response = chat_completion.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Clear the input field after submitting
    st.session_state.clear_input = True

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"] or ' ')