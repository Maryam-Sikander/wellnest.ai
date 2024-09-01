import streamlit as st
from streamlit_option_menu import option_menu
from wellness_analytics import WellnessAnalytics
from journal import interactive_gratitude_journal  
from groq_response import initialize_chat, generate_response, voice_to_text
import base64

# Initialize the WellnessAnalytics instance
analytics = WellnessAnalytics()

# ------------------------- LOGO -------------------------------

# Convert the image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
image_base64 = get_base64_image("WELLNEST.png")

# ------------------------- CSS -------------------------------
st.markdown(
    f"""
    <style>
    [data-testid="stSidebar"] {{
        background-color: #71bac7; 
        background-image: url("data:image/png;base64,{image_base64}");
        background-repeat: no-repeat;
        background-position: center top;
        background-size: 280px 280px; 
        padding-top: 170px; 
    }}
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #71bac7; 
        font-family: Arial, sans-serif; 
    }
    .nav-tabs {
        background-color: #71bac7; 
    }
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .stButton > button {
        width: 190px;
        background-color: #4CAF50;
        color: white;
    }
    .water-drop {
        font-size: 24px;
        margin-right: 5px;
    }
    .gratitude-prompt {
        font-style: italic;
        color: #666;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------- Sidebar Tabs -------------------------------
with st.sidebar:
    selected_tab = option_menu(
        menu_title=None,
        options=["Wellness Chat", "Wellness Tracking", "Gratitude Journal"],
        icons=["chat-text", "award", "book"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",  
        styles={
            "container": {"padding": "0!important", "background-color": "#71bac7"},
            "icon": {"color": "black", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#b0ebf5"},
        }
    )

# ------------------------- CHatBot -------------------------------

initialize_chat()
# Wellness Plans tab
if selected_tab == "Wellness Chat":
    initialize_chat()
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message(message["role"], avatar="👩‍💻"):
                st.markdown(message["content"])
        elif message["role"] == "assistant":
            with st.chat_message(message["role"], avatar="🕊️"):
                st.markdown(message["content"])

    # Accept user input and generate response
    if prompt := st.chat_input("Let's talk about your wellness!"):
        generate_response(prompt)

    # Voice input option
    if st.button("Speak"):
        voice_input = voice_to_text()
        if voice_input:
            generate_response(voice_input)

# ------------------------- Wellness Tracking  -------------------------------
elif selected_tab == "Wellness Tracking":
    analytics.display_wellness_tracking()

# ------------------------- Journal tab -------------------------------
elif selected_tab == "Gratitude Journal":
    interactive_gratitude_journal()  # Call the journal feature
