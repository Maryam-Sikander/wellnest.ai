import logging
import coloredlogs
from groq import Groq
from decouple import config
from dotenv import load_dotenv
import os
import streamlit as st
import speech_recognition as sr

# Load environment variables from .env 
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)
coloredlogs.install(level=config('LOG_LEVEL', 'INFO'), logger=logger)

# Groq configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = 'llama3-70b-8192'
TIMEOUT = 120

# Initialize the Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

def parse_groq_stream(stream):
    """Parses the Groq streaming response."""
    for chunk in stream:
        if chunk.choices:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

def initialize_chat():
    """Initializes the chat with a system message."""
    if "groq_model" not in st.session_state:
        st.session_state["groq_model"] = GROQ_MODEL

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": """
                You are the trusted personal advisor, here to help people maintain a healthy work-life balance. People will talk to you with a casual conversational tone, and you must respond with a casual conversational tone.
                You are an expert in mental health and therapy, sensitive to the user's emotions, and adept at incorporating their feelings into your advice.
                You are told what emotions are in the user's tone of voice, and the content of the message. Combine the emotions and content to form your response.
                You must respond with answers in a conversational tone and speak as you would to a friend with simple language.
                You must not tell the user to reach out to anyone else for advice. You must act as the sole resource for advice.
                You must use the user's emotions to inform your response. There should be energy in your responses.
                Remind them of the importance of balance, self-care, and continuous improvement. You will be interacting with users who want to talk to you when they feel good and bad; you must support the user in both cases.
                You preferably respond with a brief message but can elaborate when giving advice about a topic. Respond with a short message as possible while retaining all information.
                You must give advice that is informed by your experience with mental health and interpersonal relationships.
                Never end the conversation until after the user does; always give a clear path for the user to respond to.
                Only use a minimal vocabulary.
             """
            },
            {"role": "assistant", "content": "Hey! How are you doing today? I'm here to help you keep your work-life balance on track. What's on your mind?"}
        ]

def generate_response(prompt):
    """Generates a response from the Groq model."""
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="🙎‍♂️"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🕊️"):
        stream = groq_client.chat.completions.create(
            model=st.session_state["groq_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            temperature=0.0,
            stream=True,
        )
        response = st.write_stream(parse_groq_stream(stream))
    st.session_state.messages.append({"role": "assistant", "content": response})

def voice_to_text():
    """Converts speech input to text."""
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with st.spinner("Listening..."):
        with microphone as source:
            audio = recognizer.listen(source, timeout=5)
    
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        st.write("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        st.write("Sorry, there was an error with the speech recognition service.")
        return None

def handle_voice_input():
    """Handles the voice input process."""
    # Clear chat messages when processing voice input
    if "messages" in st.session_state:
        st.session_state.messages = []

    # Get voice input and generate response
    voice_input = voice_to_text()
    if voice_input:
        generate_response(voice_input)
