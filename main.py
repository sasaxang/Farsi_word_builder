import streamlit as st
from app_fa import run_app as run_fa
from app_en import run_app as run_en

st.set_page_config(page_title="Persian Word Spinner", layout="centered")

# Language toggle
lang = st.radio("🌐 Language", ["فا", "EN"], horizontal=True)
is_farsi = lang == "فا"

# Run selected UI
if is_farsi:
    run_fa(is_farsi=True)
else:
    run_en(is_farsi=False)
