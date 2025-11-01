import streamlit as st
import random
import os
from utils.loader import load_affixes_json, load_affixes_excel, save_affixes_json

DATA_PATH = "data/affixes.json"

st.set_page_config(page_title="سازنده واژه فارسی", layout="centered")

st.title("🧪 سازنده واژه فارسی")
st.caption("ساخت واژه‌های تصادفی با ترکیب پیشوند، ریشه و پسوند")

# Load affixes
if not os.path.exists(DATA_PATH):
    st.error("فایل affixes.json پیدا نشد.")
    st.stop()

affixes = load_affixes_json(DATA_PATH)

# Word generation
st.header("🎲 ساخت واژه تصادفی")
count = st.slider("تعداد واژه‌ها", 1, 20, 5)
generated = []

for _ in range(count):
    prefix = random.choice(affixes["prefixes"]) if affixes["prefixes"] else ""
    root = random.choice(affixes["roots"]) if affixes["roots"] else ""
    suffix = random.choice(affixes["suffixes"]) if affixes["suffixes"] else ""
    word = f"{prefix}{root}{suffix}"
    generated.append(word)

st.write("واژه‌های ساخته‌شده:")
st.code("\n".join(generated), language="text")

# Add new affix
st.header("➕ افزودن وند جدید")
with st.form("add_affix"):
    new_prefix = st.text_input("پیشوند جدید")
    new_root = st.text_input("ریشه جدید")
    new_suffix = st.text_input("پسوند جدید")
    submitted = st.form_submit_button("افزودن")

    if submitted:
        if new_prefix:
            affixes["prefixes"].append(new_prefix)
        if new_root:
            affixes["roots"].append(new_root)
        if new_suffix:
            affixes["suffixes"].append(new_suffix)
        save_affixes_json(DATA_PATH, affixes)
        st.success("وندها با موفقیت اضافه شدند. برای دیدن تغییرات، صفحه را رفرش کنید.")

# Upload affix file
st.header("📤 بارگذاری فایل وندها")
uploaded_file = st.file_uploader("فایل Excel یا JSON را آپلود کنید", type=["xlsx", "json"])

if uploaded_file:
    if uploaded_file.name.endswith(".json"):
        new_data = load_affixes_json(uploaded_file)
    else:
        new_data = load_affixes_excel(uploaded_file)

    affixes["prefixes"].extend(new_data.get("prefixes", []))
    affixes["roots"].extend(new_data.get("roots", []))
    affixes["suffixes"].extend(new_data.get("suffixes", []))
    save_affixes_json(DATA_PATH, affixes)
    st.success("وندهای جدید از فایل اضافه شدند.")
