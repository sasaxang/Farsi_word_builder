import streamlit as st
from core.word_builder import combine_affixes

def affix_select_ui(affixes, lang="fa"):
    labels = {
        "fa": {"prefix": "پیشوند", "root": "ریشه", "suffix": "پسوند"},
        "en": {"prefix": "Prefix", "root": "Root", "suffix": "Suffix"}
    }

    col1, col2, col3 = st.columns(3)
    with col1:
        st.selectbox(labels[lang]["prefix"], affixes["prefixes"], key="selected_prefix", on_change=update_word)
    with col2:
        st.selectbox(labels[lang]["root"], affixes["roots"], key="selected_root", on_change=update_word)
    with col3:
        st.selectbox(labels[lang]["suffix"], affixes["suffixes"], key="selected_suffix", on_change=update_word)

def update_word():
    word = combine_affixes(
        st.session_state.selected_prefix,
        st.session_state.selected_root,
        st.session_state.selected_suffix
    )
    st.session_state.word_parts = {
        "prefix": st.session_state.selected_prefix,
        "root": st.session_state.selected_root,
        "suffix": st.session_state.selected_suffix,
        "word": word
    }

def display_word():
    st.markdown("---")
    st.markdown(f"<div class='fancy-word'>{st.session_state.word_parts['word']}</div>", unsafe_allow_html=True)
