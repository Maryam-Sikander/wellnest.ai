import streamlit as st
from datetime import datetime
import pandas as pd
import random


# Custom CSS to improve the look and feel
st.markdown("""
<style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
        width: 100%;
    }
    .stButton > button {
        width: 100%;
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
    .input-icon {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
    }
    .input-icon span {
        font-size: 20px;
        margin-right: 8px;
    }
</style>
""", unsafe_allow_html=True)

def get_gratitude_prompt():
    prompts = [
        "What made you smile today?",
        "Who are you thankful for and why?",
        "What's something beautiful you saw today?",
        "What's a small win you had recently?",
        "What is something I am grateful to have learned?",
        "What is a talent or skill that I'm grateful to possess?",
        "What about my health am I thankful for?",
        "What about my financial situation am I grateful for?",
        "What's something you're looking forward to?",
        "What's a challenge you overcame recently?",
        "What's something you love about yourself?",
        "What's a kind gesture someone did for you lately?",
    ]
    return random.choice(prompts)

def interactive_gratitude_journal():
    st.subheader("🌟 Daily Gratitude Journal")

    # Date display
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"{datetime.now().strftime('%A, %B %d, %Y')}")
    with col2:
        if st.button("➕ New Entry"):
            st.session_state.gratitudes = ["", "", ""]
            st.session_state.water_intake = 0
            st.session_state.look_forward = ""
            st.experimental_rerun()

    st.markdown("---")

    # Initialize gratitude entries in session state
    if 'gratitudes' not in st.session_state:
        st.session_state.gratitudes = ["", "", ""]

    # Gratitude entries
    st.markdown("#### TODAY I'M GRATEFUL FOR:")
    prompts = [get_gratitude_prompt() for _ in range(3)]
    
    for i in range(3):
        st.session_state.gratitudes[i] = st.text_input(
            f"Gratitude {i+1}", 
            placeholder=prompts[i], 
            value=st.session_state.gratitudes[i], 
            key=f"gratitude_{i}",
            on_change=lambda i=i: st.session_state.gratitudes.__setitem__(i, st.session_state[f"gratitude_{i}"])
        )

    st.markdown("---")

    # Water intake
    st.markdown("#### WATER INTAKE")
    if 'water_intake' not in st.session_state:
        st.session_state.water_intake = 0

    col1, col2 = st.columns([3, 1])
    with col1:
        water_intake = st.slider("Glasses of water", 0, 8, st.session_state.water_intake)
    with col2:
        st.markdown(f'<h1>{"💧" * water_intake}</h1>', unsafe_allow_html=True)
    st.session_state.water_intake = water_intake

    st.markdown("---")

    # Tomorrow's look forward
    st.markdown("#### TOMORROW I LOOK FORWARD TO:")
    if 'look_forward' not in st.session_state:
        st.session_state.look_forward = ""
    st.session_state.look_forward = st.text_area("", value=st.session_state.look_forward, height=100)

    # Save entry
    if st.button("Save Today's Reflections"):
        entry = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Gratitude 1": st.session_state.gratitudes[0],
            "Gratitude 2": st.session_state.gratitudes[1],
            "Gratitude 3": st.session_state.gratitudes[2],
            "Water Intake": st.session_state.water_intake,
            "Look Forward": st.session_state.look_forward
        }

        if 'journal_entries' not in st.session_state:
            st.session_state.journal_entries = pd.DataFrame(columns=entry.keys())

        st.session_state.journal_entries = pd.concat([st.session_state.journal_entries, pd.DataFrame([entry])], ignore_index=True)
        st.success("Your reflections have been saved! 🎉")

    # View  entries
    if st.checkbox("View Journey of Gratitude"):
        if 'journal_entries' in st.session_state and not st.session_state.journal_entries.empty:
            st.dataframe(st.session_state.journal_entries.style.highlight_max(axis=0))
        else:
            st.info("Your gratitude journey is just beginning. Make your first entry to start!")

if __name__ == "__main__":
    interactive_gratitude_journal()
