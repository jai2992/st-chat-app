import streamlit as st
import pandas as pd
import groq
import os
import time
import numpy as np
from langchain_groq import ChatGroq  # Assuming you use LangChain for summary

st.title("Chat with Llama")

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

# Button to trigger summarization in the sidebar
if st.sidebar.button("Generate Summary"):
    st.session_state.show_summary = True  # Set flag to show summary
else:
    st.session_state.show_summary = False

def stream_data(txt):
    for word in txt.split(" "):
        yield word + " "
        time.sleep(0.05)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "edited_index" not in st.session_state:
    st.session_state.edited_index = None  # For tracking which message to edit
if "summary" not in st.session_state:
    st.session_state.summary = ""  # Store summarized chat history
if "show_summary" not in st.session_state:
    st.session_state.show_summary = False  # Control whether to show summary

# Function to summarize long chat history using LangChain
def summarize_chat_history(history):
    llm = ChatGroq(
    temperature=0,
    model=selected_model,
    api_key=st.secrets["GROQ_API_KEY"]
    )  # LangChain model for summarization, adjust based on your setup
    conversation_text = "\n".join([msg["content"] for msg in history if msg["role"] == "user" or msg["role"] == "assistant"])
    
    # Only summarize if conversation length exceeds a threshold
    if len(conversation_text) > 1000:  # You can adjust this threshold
        summary = llm.run(conversation_text)
        return summary
    return ""

# Display chat history
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    
    # Show "Edit" button for user messages
    if message["role"] == "user":
        if st.button(f"Edit", key=f"edit_{i}"):
            st.session_state.edited_index = i  # Set the index to edit
            break  # Stop the chat display so that the history rewinds after editing

# Input box for user prompt (without `value` argument)
prompt = st.chat_input("What is up?")

if prompt:
    if st.session_state.edited_index is not None:
        # If editing, replace the message at the edited index
        st.session_state.messages[st.session_state.edited_index]["content"] = prompt
        st.session_state.edited_index = None  # Reset edit mode
    else:
        # If not editing, add the message as a new input
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

# Trigger summarization when the button is clicked
if st.session_state.show_summary:
    st.session_state.summary = summarize_chat_history(st.session_state.messages)
    with st.expander("Chat Summary"):
        st.markdown(st.session_state.summary)