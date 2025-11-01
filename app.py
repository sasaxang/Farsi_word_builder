import streamlit as st
import random
import os
from utils.loader import load_affixes_json, load_affixes_excel, save_affixes_json

DATA_PATH = "data/affixes.json"

st.set_page_config(page_title="گردونه واژه‌ساز فارسی", layout="centered")

st.markdown("""
    <style>
    body, div, input, textarea, label {
        direction: rtl;
        text-align: right;
        font-family: "Vazir", "Tahoma", sans-serif;
    }
    .stTextInput > div > div > input {
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

st.title("گردونه واژه‌ساز فارسی")
st.caption("ساخت واژه‌های تصادفی با ترکیب پیشوند، ریشه و پسوند")

# Load affixes
if not os.path.exists(DATA_PATH):
    st.error("فایل وندها پیدا نشد.")
    st.stop()

affixes = load_affixes_json(DATA_PATH)

# گردونه واژه‌ساز
st.header("بچرخون گردونه!")

if st.button("بچرخون!"):
    prefix = random.choice(affixes["prefixes"]) if affixes["prefixes"] else ""
    root = random.choice(affixes["roots"]) if affixes["roots"] else ""
    suffix = random.choice(affixes["suffixes"]) if affixes["suffixes"] else ""
    word = f"{prefix}{root}{suffix}"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("پیشوند")
        st.success(prefix)
    with col2:
        st.subheader("ریشه")
        st.info(root)
    with col3:
        st.subheader("پسوند")
        st.warning(suffix)

    st.markdown("---")
    st.subheader("واژه ساخته‌شده:")
    st.code(word, language="text")

# افزودن وند جدید
st.header("افزودن وند جدید")
with st.form("add_affix"):
    new_prefix = st.text_input("پیشوند جدید")
    new_root = st.text_input("ریشه جدید")
    new_suffix = st.text_input("پسوند جدید")
    submitted = st.form_submit_button("افزودن")

    if submitted:
        if new_prefix and new_prefix not in affixes["prefixes"]:
            affixes["prefixes"].append(new_prefix)
        if new_root and new_root not in affixes["roots"]:
            affixes["roots"].append(new_root)
        if new_suffix and new_suffix not in affixes["suffixes"]:
            affixes["suffixes"].append(new_suffix)
        save_affixes_json(DATA_PATH, affixes)
        st.success("وندها با موفقیت اضافه شدند.")

# حذف وندها
st.header("حذف وندها")
delete_type = st.selectbox("نوع وند برای حذف", ["پیشوند", "ریشه", "پسوند"])
to_delete = st.selectbox("انتخاب وند برای حذف", affixes[{"پیشوند": "prefixes", "ریشه": "roots", "پسوند": "suffixes"}[delete_type]])

if st.button("حذف وند"):
    affixes[{"پیشوند": "prefixes", "ریشه": "roots", "پسوند": "suffixes"}[delete_type]].remove(to_delete)
    save_affixes_json(DATA_PATH, affixes)
    st.success(f"وند «{to_delete}» حذف شد.")

# ویرایش وند
st.header("ویرایش وند")
edit_type = st.selectbox("نوع وند برای ویرایش", ["پیشوند", "ریشه", "پسوند"])
original = st.selectbox("انتخاب وند", affixes[{"پیشوند": "prefixes", "ریشه": "roots", "پسوند": "suffixes"}[edit_type]])
new_value = st.text_input("مقدار جدید")

if st.button("ویرایش وند"):
    lst = affixes[{"پیشوند": "prefixes", "ریشه": "roots", "پسوند": "suffixes"}[edit_type]]
    idx = lst.index(original)
    lst[idx] = new_value
    save_affixes_json(DATA_PATH, affixes)
    st.success(f"وند «{original}» به «{new_value}» تغییر یافت.")

# بارگذاری فایل وندها
st.header("بارگذاری فایل وندها")
uploaded_file = st.file_uploader("فایل Excel یا JSON را آپلود کنید", type=["xlsx", "json"])

if uploaded_file:
    if uploaded_file.name.endswith(".json"):
        new_data = load_affixes_json(uploaded_file)
    else:
        new_data = load_affixes_excel(uploaded_file)

    affixes["prefixes"].extend([p for p in new_data.get("prefixes", []) if p not in affixes["prefixes"]])
    affixes["roots"].extend([r for r in new_data.get("roots", []) if r not in affixes["roots"]])
    affixes["suffixes"].extend([s for s in new_data.get("suffixes", []) if s not in affixes["suffixes"]])
    save_affixes_json(DATA_PATH, affixes)
    st.success("وندهای جدید از فایل اضافه شدند.")
