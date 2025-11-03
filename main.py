import streamlit as st
from app_fa import run_app as run_fa
from app_en import run_app as run_en

# Set page configuration
st.set_page_config(page_title="Farsi Word Builder", layout="centered")

# Display compact language selector in top-left corner
col_lang, col_title = st.columns([1, 5])
with col_lang:
    lang = st.selectbox("", ["فارسی", "English"], key="language", label_visibility="collapsed")
is_farsi = lang == "فارسی"

# Display responsive app title with minimal top margin
with col_title:
    st.markdown(f"""
    <div style="margin-top:-0.5rem; margin-bottom:0; display:flex; flex-direction:column; align-items:center; justify-content:center;">
        <div style="font-size:clamp(1.2rem, 4vw, 2rem); white-space:nowrap; margin-bottom:0;">
            {'گردونه واژه‌ساز فارسی' if is_farsi else 'Persian Word Spinner'}
        </div>
        <div style="font-size:clamp(0.9rem, 3vw, 1.2rem); color:gray; margin-top:-0.2rem;">
            {'ساخت واژه‌های تصادفی با ترکیب پیشوند، ریشه و پسوند' if is_farsi else 'Generate random Persian words by combining prefix, root, and suffix'}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Run the appropriate app based on selected language
if is_farsi:
    run_fa(is_farsi=True)
else:
    run_en(is_farsi=False)
