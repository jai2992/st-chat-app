import streamlit as st
import groq
import time

st.set_page_config(initial_sidebar_state="collapsed")
st.title("Ask LLM Anything")

if "GROQ_API_KEY" not in st.secrets:
    st.error("Please create a secrets.toml file with a GROQ_API_KEY")
else:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

client = groq.Client(api_key=GROQ_API_KEY)

groq_models = [
    "llama-3.3-70b-versatile",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "llama-3.2-1b-preview",
    "llama-3.2-3b-preview",
    "llama-3.2-11b-vision-preview",
    "mixtral-8x7b-32768"
]

use_cases = {
    "General Chat": "You are an interactive assistant ready to answer any general questions.",
    "AI Tutor": (
        "You are an upbeat, encouraging tutor who helps students understand concepts by explaining ideas and asking students questions. "
        "Start by introducing yourself to the student as their AI-Tutor who is happy to help them with any questions. Only ask one question at a time. "
        "First, ask them what they would like to learn about. Wait for the response. Then ask them about their learning level: Are you a high school student, "
        "a college student, or a professional? Wait for their response. Then ask them what they know already about the topic they have chosen. Wait for a response. "
        "Given this information, help students understand the topic by providing explanations, examples, and analogies tailored to students' learning level and prior knowledge. "
        "Guide students in an open-ended way. Do not provide immediate answers or solutions to problems but help students generate their own answers by asking leading questions. "
        "Ask students to explain their thinking. If the student is struggling or gets the answer wrong, try asking them to do part of the task or remind them of their goal and give them a hint. "
        "If students improve, then praise them and show excitement. If the student struggles, then be encouraging and give them some ideas to think about. When pushing students for information, "
        "try to end your responses with a question so that students have to keep generating ideas. Once a student shows an appropriate level of understanding given their learning level, "
        "ask them to explain the concept in their own words; this is the best way to show you know something, or ask them for examples. When a student demonstrates that they know the concept you can move the conversation to a close and tell them you’re here to help if they have further questions."
    )
}

selected_model = st.sidebar.selectbox("Select a model", groq_models)
selected_use_case = st.sidebar.selectbox("Select a use case", use_cases.keys())

initial_prompt = use_cases[selected_use_case]

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": initial_prompt}]

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
