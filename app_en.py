import streamlit as st
import random
from core.affix_manager import load_affixes, save_affixes, merge_affixes
from core.ui_components import affix_select_ui, update_word, display_word
from utils.loader import save_affixes_json


def run_app(is_farsi: bool):
    DATA_PATH = "data/affixes.json"
    st.set_page_config(page_title="Persian Word Spinner", layout="centered")

    # ✅ Inject custom CSS
    st.markdown("""
        <style>
        .fancy-word {
            text-align: center;
            direction: lrt;
            font-size: 48px;
            font-weight: bold;
            color: #ffffff;
            background-color: #4A90E2;
            padding: 12px 24px;
            border-radius: 12px;
            font-family: "Vazir", "Comic Sans MS", cursive;
            animation: pop 0.6s ease-out;
        }

        @keyframes pop {
            0% { transform: scale(0.8); opacity: 0.5; }
            100% { transform: scale(1); opacity: 1; }
        }

        </style>
    """, unsafe_allow_html=True)

    st.title("گردونه واژه‌ساز فارسی" if is_farsi else "Persian Word Spinner")
    st.caption("ساخت واژه‌های تصادفی با ترکیب پیشوند، ریشه و پسوند" if is_farsi else "Generate random Persian words by combining prefix, root, and suffix")


    affixes = load_affixes(DATA_PATH)

    # Initialize selections
    for key, lst in [("selected_prefix", "prefixes"), ("selected_root", "roots"), ("selected_suffix", "suffixes")]:
        if key not in st.session_state:
            st.session_state[key] = affixes[lst][0] if affixes[lst] else ""

    if "word_parts" not in st.session_state:
        update_word()

    def spin_random(affixes):
        st.session_state.selected_prefix = random.choice(affixes["prefixes"]) if affixes["prefixes"] else ""
        st.session_state.selected_root = random.choice(affixes["roots"]) if affixes["roots"] else ""
        st.session_state.selected_suffix = random.choice(affixes["suffixes"]) if affixes["suffixes"] else ""
        update_word()

    # Affix selection UI
    affix_select_ui(affixes, lang="fa" if is_farsi else "en")

    # Random word generation button
    st.button("تصادفی بساز!" if is_farsi else "Spin Random!", on_click=lambda: spin_random(affixes))

    # Display the generated word
    display_word()

    # Toggle to show the add affix form
    if st.button("➕ افزودن وند" if is_farsi else "➕ Add Affix"):
        st.session_state.show_add_form = True

    # Add affix form
    if st.session_state.get("show_add_form"):
        with st.form("add_affix"):
            new_prefix = st.text_input("پیشوند جدید" if is_farsi else "New Prefix")
            new_root = st.text_input("ریشه جدید" if is_farsi else "New Root")
            new_suffix = st.text_input("پسوند جدید" if is_farsi else "New Suffix")
            submitted = st.form_submit_button("افزودن" if is_farsi else "Add")

            if submitted:
                added = False
                if new_prefix and new_prefix not in affixes["prefixes"]:
                    affixes["prefixes"].append(new_prefix)
                    added = True
                if new_root and new_root not in affixes["roots"]:
                    affixes["roots"].append(new_root)
                    added = True
                if new_suffix and new_suffix not in affixes["suffixes"]:
                    affixes["suffixes"].append(new_suffix)
                    added = True

                if added:
                    save_affixes_json(DATA_PATH, affixes)
                    st.success("وندها با موفقیت اضافه شدند." if is_farsi else "Affixes added successfully.")
                else:
                    st.warning("هیچ وند جدیدی اضافه نشد." if is_farsi else "No new affix was added.")

                st.session_state.show_add_form = False

