import streamlit as st
from core.word_builder import combine_affixes

def affix_select_ui(affixes, lang="fa"):
    # Define UI labels for Persian and English, including affix names and word structure
    labels = {
        "fa": {
            "prefix": "پیشوند",
            "root": "ریشه",
            "suffix": "پسوند",
            "lock": "ثابت نگه‌دار",
            "structure": "ساختار واژه"
        },
        "en": {
            "prefix": "Prefix",
            "root": "Root",
            "suffix": "Suffix",
            "lock": "Lock",
            "structure": "Word Structure"
        }
    }

    # Define word structure options for both languages
    structure_options = {
        "fa": ["پیشوند + ریشه (مثل: بی‌گربه)", "ریشه + پسوند (مثل: گربه‌گاه)", "پیشوند + ریشه + پسوند (مثل: خویش‌گربه‌پرداز)"],
        "en": ["Prefix + Root (e.g. بی‌گربه)", "Root + Suffix (e.g. گربه‌گاه)", "Prefix + Root + Suffix (e.g. خویش‌گربه‌پرداز)"]
    }

    # Display word structure selector above affix selectors
    structure = st.selectbox(
        labels[lang]["structure"],
        structure_options[lang],
        index=2,
        key="word_structure"
    )

    # Determine which components should be disabled based on structure
    disable_prefix = structure in ["ریشه + پسوند (مثل: گربه‌گاه)", "Root + Suffix (e.g. گربه‌گاه)"]
    disable_suffix = structure in ["پیشوند + ریشه (مثل: بی‌گربه)", "Prefix + Root (e.g. بی‌گربه)"]

    # Display affix selectors with lock checkboxes in rows (better for mobile)
    # Layout: [Label] [Dropdown] [Lock]
    
    # Helper to render a row
    def render_row(label, items, key_prefix, key_lock, on_change_func, disabled=False):
        c1, c2, c3 = st.columns([1.5, 4, 1.5])
        
        with c1:
            # Vertical alignment hack using markdown with some top margin/padding if needed
            # or just simple text. Using subheader or markdown for bold text.
            st.markdown(f"<p style='font-weight:bold; margin:0;'>{label}</p>", unsafe_allow_html=True)
            
        with c2:
            st.selectbox(
                label, # Hidden but good for accessibility if screen reader reads it
                items,
                key=key_prefix,
                on_change=on_change_func,
                disabled=disabled,
                label_visibility="collapsed"
            )
            
        with c3:
            # Checkbox for lock
            st.checkbox(labels[lang]["lock"], key=key_lock, disabled=disabled)

    # Prefix Row
    render_row(
        labels[lang]["prefix"],
        [""] + affixes["prefixes"],
        "selected_prefix",
        "lock_prefix",
        update_word,
        disable_prefix
    )

    # Root Row
    render_row(
        labels[lang]["root"],
        affixes["roots"],
        "selected_root",
        "lock_root",
        update_word,
        False # Root is never disabled in current logic
    )

    # Suffix Row
    render_row(
        labels[lang]["suffix"],
        [""] + affixes["suffixes"],
        "selected_suffix",
        "lock_suffix",
        update_word,
        disable_suffix
    )

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
