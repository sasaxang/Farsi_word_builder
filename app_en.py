import streamlit as st
import random
from core.affix_manager import load_affixes, save_affixes, merge_affixes
from core.ui_components import affix_select_ui, update_word, display_word
from utils.loader import save_affixes_json
import re
from core.word_builder import combine_affixes


def is_farsi_text(text):
    """Check if the input contains at least one Persian character."""
    return bool(re.search(r'[\u0600-\u06FF]', text))

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
            margin-bottom: 32px;
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
        # Always include root
        root = random.choice(affixes["roots"]) if affixes["roots"] else ""

        # Randomly decide whether to include prefix and suffix
        include_prefix = random.choice([True, False])
        include_suffix = random.choice([True, False])

        # ✅ Ensure at least one of prefix or suffix is included
        if not include_prefix and not include_suffix:
            # Randomly force one of them to be True
            if random.choice(["prefix", "suffix"]) == "prefix":
                include_prefix = True
            else:
                include_suffix = True

        # Assign values
        st.session_state.selected_prefix = (
            random.choice(affixes["prefixes"]) if include_prefix and affixes["prefixes"] else ""
        )
        st.session_state.selected_root = root
        st.session_state.selected_suffix = (
            random.choice(affixes["suffixes"]) if include_suffix and affixes["suffixes"] else ""
        )

        update_word()

    # Affix selection UI
    affix_select_ui(affixes, lang="fa" if is_farsi else "en")

    # Display the generated word
    display_word()

    # Random word generation button
    st.button("تصادفی بساز!" if is_farsi else "Spin Random!", on_click=lambda: spin_random(affixes))

    # Toggle to show the add affix form
    if st.button("➕ افزودن وند" if is_farsi else "➕ Add Affix"):
        st.session_state.show_add_form = True

    # Add affix form
    if st.session_state.get("show_add_form", True):  # default to open
        with st.form("add_affix"):
            new_prefix = st.text_input("پیشوند جدید" if is_farsi else "New Prefix")
            new_root = st.text_input("ریشه جدید" if is_farsi else "New Root")
            new_suffix = st.text_input("پسوند جدید" if is_farsi else "New Suffix")

            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("✅ افزودن" if is_farsi else "✅ Add")
            with col2:
                close = st.form_submit_button("❌ بستن فرم" if is_farsi else "❌ Close Form")

            if close:
                st.session_state.show_add_form = False

            elif submitted:
                errors = []
                invalid_fields = []

                if new_prefix and not is_farsi_text(new_prefix):
                    invalid_fields.append("پیشوند" if is_farsi else "Prefix")
                if new_root and not is_farsi_text(new_root):
                    invalid_fields.append("ریشه" if is_farsi else "Root")
                if new_suffix and not is_farsi_text(new_suffix):
                    invalid_fields.append("پسوند" if is_farsi else "Suffix")

                if invalid_fields:
                    if is_farsi:
                        msg = f"{'، '.join(invalid_fields)} باید فارسی {'باشد' if len(invalid_fields)==1 else 'باشند'}."
                    else:
                        msg = f"{', '.join(invalid_fields)} must be in Persian."
                    st.error(msg)
                else:
                    added_prefix = new_prefix and new_prefix not in affixes["prefixes"]
                    added_root   = new_root and new_root not in affixes["roots"]
                    added_suffix = new_suffix and new_suffix not in affixes["suffixes"]

                    added_items = []

                    if added_prefix:
                        affixes["prefixes"].append(new_prefix)
                        added_items.append("prefix")
                    if added_root:
                        affixes["roots"].append(new_root)
                        added_items.append("root")
                    if added_suffix:
                        affixes["suffixes"].append(new_suffix)
                        added_items.append("suffix")

                    if added_items:
                        save_affixes_json(DATA_PATH, affixes)

                        count_roots = added_items.count("root")
                        count_affixes = added_items.count("prefix") + added_items.count("suffix")

                        if is_farsi:
                            root_msg = ""
                            affix_msg = ""

                            if count_roots == 1:
                                root_msg = "ریشه با موفقیت اضافه شد."
                            elif count_roots > 1:
                                root_msg = "ریشه‌ها با موفقیت اضافه شدند."

                            if count_affixes == 1:
                                affix_msg = "وند با موفقیت اضافه شد."
                            elif count_affixes > 1:
                                affix_msg = "وندها با موفقیت اضافه شدند."

                            final_msg = " ".join([msg for msg in [affix_msg, root_msg] if msg])
                        else:
                            root_msg = ""
                            affix_msg = ""

                            if count_roots == 1:
                                root_msg = "Root added successfully."
                            elif count_roots > 1:
                                root_msg = "Roots added successfully."

                            if count_affixes == 1:
                                affix_msg = "Affix added successfully."
                            elif count_affixes > 1:
                                affix_msg = "Affixes added successfully."

                            final_msg = " ".join([msg for msg in [affix_msg, root_msg] if msg])

                        st.success(final_msg)
                    else:
                        st.warning("هیچ وند یا ریشه‌ای اضافه نشد." if is_farsi else "No affix or root was added.")
