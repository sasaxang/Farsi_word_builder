import streamlit as st
from app_fa import run_app as run_fa
from app_en import run_app as run_en

# Set page configuration
st.set_page_config(page_title="Farsi Word Builder", layout="centered")

# Initialize language state
if "language" not in st.session_state:
    st.session_state.language = "فا"  # Default to Persian

is_farsi = st.session_state.language == "فا"

# Centered language toggle button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    toggle_label = "🇮🇷 تغییر به انگلیسی" if is_farsi else "🇬🇧 Switch to Persian"
    if st.button(toggle_label):
        st.session_state.language = "EN" if is_farsi else "فا"
        st.rerun()

# Run the appropriate app based on selected language
if st.session_state.language == "فا":
    run_fa(is_farsi=True)
else:
    run_en(is_farsi=False)
