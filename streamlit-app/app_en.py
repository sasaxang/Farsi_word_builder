import streamlit as st
import random
from core.affix_manager import load_affixes, save_affixes, merge_affixes
from core.ui_components import affix_select_ui, update_word, display_word
from utils.loader import save_affixes_json
from utils.combinations import calculate_total_combinations, convert_to_persian_numerals
import re
from core.word_builder import combine_affixes


def is_farsi_text(text):
    """Check if the input contains at least one Persian character."""
    return bool(re.search(r'[\u0600-\u06FF]', text))

import os

def run_app(is_farsi: bool):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(current_dir, "data", "affixes.json")
    st.set_page_config(page_title="Persian Word Spinner", layout="centered")

    # ✅ Inject custom CSS
    st.markdown("""
        <style>
        /* Custom Color Theme */
        :root {
            --bg-cream: #F5F1E8;
            --accent-orange: #F39C12;
            --text-dark: #1A1A1A;
            --grid-color: rgba(0, 0, 0, 0.05);
        }
        
        /* Background with grid pattern */
        .stApp {
            background-color: var(--bg-cream);
            background-image: 
                linear-gradient(var(--grid-color) 1px, transparent 1px),
                linear-gradient(90deg, var(--grid-color) 1px, transparent 1px);
            background-size: 20px 20px;
        }
        
        /* Override Streamlit's default background */
        .main {
            background-color: transparent;
        }
        
        .fancy-word {
            text-align: center;
            direction: lrt;
            font-size: clamp(24px, 8vw, 48px);
            font-weight: bold;
            color: #ffffff;
            background-color: var(--accent-orange);
            padding: 12px 24px;
            border-radius: 12px;
            font-family: "Vazir", "Comic Sans MS", cursive;
            animation: pop 0.6s ease-out;
            margin-bottom: 32px;
            word-break: keep-all;
            overflow-wrap: normal;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 100%;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        @keyframes pop {
            0% { transform: scale(0.8); opacity: 0.5; }
            100% { transform: scale(1); opacity: 1; }
        }

        </style>
        
        <style>
        /* Reduce padding for compact mobile view */
        .block-container {
            padding-top: 4.5rem !important;
            padding-bottom: 1rem !important;
        }
        
        /* Align checkbox vertically */
        div[data-testid="stCheckbox"] {
            padding-top: 8px;
        }
        
        /* Add spacing between checkbox label and checkbox */
        div[data-testid="stCheckbox"] label {
            gap: 0.5rem;
        }
        
        /* Compact rows */
        div[data-testid="column"] {
            padding: 0 !important;
        }

        @media (max-width: 768px) {
          /* Reduce top padding to ensure title is visible */
          .block-container {
            padding-top: 3.5rem !important;
          }
          
          /* Ensure title and language selector remain visible */
          div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-wrap: wrap !important;
          }

          /* For 3-column layouts (affix selectors), make them more compact */
          div[data-testid="column"] {
            padding: 0.2rem !important;
          }

          /* Reduce font size slightly for better fit */
          div[data-testid="stSelectbox"] label,
          div[data-testid="stCheckbox"] label {
            font-size: 0.85rem !important;
          }

          /* Prevent horizontal scroll */
          .main, .block-container {
            overflow-x: hidden !important;
          }
        }
        </style>
    """, unsafe_allow_html=True)

    affixes = load_affixes(DATA_PATH)

    # Initialize selections
    for key, lst in [("selected_prefix", "prefixes"), ("selected_root", "roots"), ("selected_suffix", "suffixes")]:
        if key not in st.session_state:
            st.session_state[key] = affixes[lst][0] if affixes[lst] else ""

    if "word_parts" not in st.session_state:
        update_word()

    def spin_random(affixes):
    # Retrieve selected word structure from session state
    # Retrieve selected word structure from session state
        structure = st.session_state.get("word_structure", "Prefix + Root + Suffix (e.g. خویش‌گربه‌پرداز)")

        # Determine which components to include based on selected structure
        include_prefix = structure in [
            "پیشوند + ریشه (مثل: بی‌گربه)", 
            "پیشوند + ریشه + پسوند (مثل: خویش‌گربه‌پرداز)", 
            "Prefix + Root (e.g. بی‌گربه)", 
            "Prefix + Root + Suffix (e.g. خویش‌گربه‌پرداز)"
        ]
        include_suffix = structure in [
            "ریشه + پسوند (مثل: گربه‌گاه)", 
            "پیشوند + ریشه + پسوند (مثل: خویش‌گربه‌پرداز)", 
            "Root + Suffix (e.g. گربه‌گاه)", 
            "Prefix + Root + Suffix (e.g. خویش‌گربه‌پرداز)"
        ]

        # Always include root
        if st.session_state.get("lock_root"):
            root = st.session_state.selected_root
        else:
            # Filter roots if suffix is locked to "انه"
            if st.session_state.get("lock_suffix") and st.session_state.selected_suffix == "انه":
                # Exclude roots ending in "ه" (unless "اه"), "ا", or "آ"
                valid_roots = [r for r in affixes["roots"] if not (
                    (r.endswith("ه") and not r.endswith("اه")) or 
                    r.endswith("ا") or 
                    r.endswith("آ")
                )]
                root = random.choice(valid_roots) if valid_roots else ""
            else:
                root = random.choice(affixes["roots"]) if affixes["roots"] else ""

        # Handle prefix
        if include_prefix:
            if st.session_state.get("lock_prefix"):
                prefix = st.session_state.selected_prefix
            else:
                prefix = random.choice(affixes["prefixes"]) if affixes["prefixes"] else ""
        else:
            prefix = ""  # Explicitly clear prefix if not included

        # Handle suffix
        if include_suffix:
            if st.session_state.get("lock_suffix"):
                suffix = st.session_state.selected_suffix
            else:
                # Filter suffixes if root ends in "ه" (but not "اه"), "ا", or "آ"
                if root and ((root.endswith("ه") and not root.endswith("اه")) or root.endswith("ا") or root.endswith("آ")):
                    valid_suffixes = [s for s in affixes["suffixes"] if s != "انه"]
                    suffix = random.choice(valid_suffixes) if valid_suffixes else ""
                else:
                    suffix = random.choice(affixes["suffixes"]) if affixes["suffixes"] else ""
        else:
            suffix = ""  # Explicitly clear suffix if not included

        # Update session state with selected components
        st.session_state.selected_prefix = prefix
        st.session_state.selected_root = root
        st.session_state.selected_suffix = suffix

        # Generate and store the final word
        update_word()

    # Affix selection UI
    affix_select_ui(affixes, lang="fa" if is_farsi else "en")

    # Display the generated word
    display_word()

    # Random word generation button with total combinations count
    # Calculate total combinations based on current structure
    current_structure = st.session_state.get("word_structure", "Prefix + Root + Suffix (e.g. خویش‌گربه‌پرداز)")
    total_combinations = calculate_total_combinations(affixes, current_structure)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Display total combinations count
        combinations_text = f"Total Possible Combinations: {total_combinations}"
        st.markdown(f"<p style='margin-top: 8px; font-size: 0.9rem;'>{combinations_text}</p>", unsafe_allow_html=True)
    
    with col2:
        st.button("تصادفی بساز!" if is_farsi else "Spin Random!", on_click=lambda: spin_random(affixes))

    # Initialize show_add_form state if not present
    if "show_add_form" not in st.session_state:
        st.session_state.show_add_form = False

    def toggle_add_form():
        st.session_state.show_add_form = not st.session_state.show_add_form

    # Toggle button with dynamic label
    if is_farsi:
        btn_label = "➖ افزودن وند" if st.session_state.show_add_form else "➕ افزودن وند"
    else:
        btn_label = "➖ Add Affix" if st.session_state.show_add_form else "➕ Add Affix"

    st.button(btn_label, on_click=toggle_add_form)

    # Add affix form
    if st.session_state.show_add_form:
        with st.form("add_affix"):
            new_prefix = st.text_input("پیشوند جدید" if is_farsi else "New Prefix")
            new_root = st.text_input("ریشه جدید" if is_farsi else "New Root")
            new_suffix = st.text_input("پسوند جدید" if is_farsi else "New Suffix")

            # Single submit button, no close button
            submitted = st.form_submit_button("✅ افزودن" if is_farsi else "✅ Add")

            if submitted:
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
                        st.rerun()
                    else:
                        st.warning("هیچ وند یا ریشه‌ای اضافه نشد." if is_farsi else "No affix or root was added.")
