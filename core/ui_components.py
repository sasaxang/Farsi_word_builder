import streamlit as st
from core.word_builder import combine_affixes

def affix_select_ui(affixes, lang="fa"):
    # Define labels for multilingual support
    labels = {
        "fa": {"prefix": "پیشوند", "root": "ریشه", "suffix": "پسوند", "lock": "🔒 ثابت نگه دار"},
        "en": {"prefix": "Prefix", "root": "Root", "suffix": "Suffix", "lock": "🔒 Lock"}
    }

    # Display affix selectors with lock checkboxes in three columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.selectbox(
            labels[lang]["prefix"],
            [""] + affixes["prefixes"],
            key="selected_prefix",
            on_change=update_word
        )
        st.checkbox(labels[lang]["lock"], key="lock_prefix")

    with col2:
        st.selectbox(
            labels[lang]["root"],
            affixes["roots"],
            key="selected_root",
            on_change=update_word
        )
        st.checkbox(labels[lang]["lock"], key="lock_root")

    with col3:
        st.selectbox(
            labels[lang]["suffix"],
            [""] + affixes["suffixes"],
            key="selected_suffix",
            on_change=update_word
        )
        st.checkbox(labels[lang]["lock"], key="lock_suffix")

def update_word():
    # Combine selected affixes into a single word and store in session state
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
    # Display a thin horizontal spacer with minimal top/bottom margin
    st.markdown("""
    <hr style='margin: 0.5rem 0; border: none; border-top: 1px solid #ccc;' />
    """, unsafe_allow_html=True)

    # Display the generated word in styled container
    st.markdown(f"<div class='fancy-word'>{st.session_state.word_parts['word']}</div>", unsafe_allow_html=True)
