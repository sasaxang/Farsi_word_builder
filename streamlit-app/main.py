import streamlit as st
from app_fa import run_app as run_fa
from app_en import run_app as run_en
from config.firebase_config import initialize_firebase
from core.auth import show_auth_ui, init_auth_state

# Set page configuration (must be first Streamlit command)
st.set_page_config(page_title="Farsi Word Builder", layout="centered")

# Initialize Firebase only once using session state
if 'firebase_initialized' not in st.session_state:
    try:
        initialize_firebase()
        st.session_state.firebase_initialized = True
    except Exception as e:
        st.error(f"Failed to initialize Firebase: {e}")
        st.stop()

# Initialize authentication state
init_auth_state()

# Add custom CSS for language toggle button
st.markdown("""
    <style>
    /* Style the language toggle button to look like a simple text link */
    button[key="lang_toggle"] {
        background-color: transparent !important;
        border: 1px solid #ccc !important;
        border-radius: 4px !important;
        padding: 0.25rem 0.5rem !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: #4A90E2 !important;
        min-height: auto !important;
    }
    
    button[key="lang_toggle"]:hover {
        background-color: #f0f0f0 !important;
        border-color: #4A90E2 !important;
    }
    
    /* Make it more compact on mobile */
    @media (max-width: 768px) {
        button[key="lang_toggle"] {
            font-size: 0.85rem !important;
            padding: 0.2rem 0.4rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize language in session state
if "language" not in st.session_state:
    st.session_state.language = "فارسی"

# Language toggle button in top-right corner
col_title, col_lang = st.columns([5, 1])

with col_lang:
    # Show opposite language as toggle option
    toggle_text = "EN" if st.session_state.language == "فارسی" else "فا"
    if st.button(toggle_text, key="lang_toggle", help="Switch language / تغییر زبان"):
        # Toggle language
        st.session_state.language = "English" if st.session_state.language == "فارسی" else "فارسی"
        st.rerun()

is_farsi = st.session_state.language == "فارسی"

# Display responsive app title with minimal top margin
with col_title:
    st.markdown(f"""
    <div style="margin-top:0; margin-bottom:0.5rem; display:flex; flex-direction:column; align-items:center; justify-content:center;">
        <div style="font-size:clamp(1rem, 4vw, 2rem); white-space:normal; text-align:center; margin-bottom:0.2rem;">
            {'گردونه واژه‌ساز فارسی' if is_farsi else 'Persian Word Spinner'}
        </div>
        <div style="font-size:clamp(0.75rem, 2.5vw, 1.2rem); color:gray; margin-top:0; text-align:center;">
            {'ساخت واژه‌های تصادفی با ترکیب پیشوند، ریشه و پسوند' if is_farsi else 'Generate random Persian words by combining prefix, root, and suffix'}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Show authentication UI in sidebar
    # --- TEMPORARY DEBUGGING ---
    # Remove this after fixing the Cloud issue
    with st.expander("🛠 Admin Debug: Check Secrets"):
        try:
            st.write("Secrets Loaded:", list(st.secrets.keys()))
            if "auth" in st.secrets:
                st.write("Auth Config Found:", list(st.secrets["auth"].keys()))
                st.write("Redirect URI configured as:", st.secrets["auth"].get("redirect_uri", "MISSING"))
            else:
                st.error("CRITICAL: [auth] section is MISSING in secrets.")
        except Exception as e:
            st.error(f"Error reading secrets: {e}")
    # ---------------------------

    show_auth_ui(lang="fa" if is_farsi else "en")

# Run the appropriate app based on selected language
if is_farsi:
    run_fa(is_farsi=True)
else:
    run_en(is_farsi=False)

