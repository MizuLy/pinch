from pathlib import Path

import streamlit as st
from summarizer import summarize, summarize_image, STYLES, LANGUAGES
from utils import read_pdf

ICON = Path(__file__).parent / "static" / "pinch-dumpling-lower-left.png"
st.set_page_config(page_title="Pinch", page_icon=str(ICON))
st.title("🥟 Pinch")

style = st.selectbox("Summary style", list(STYLES))
language = st.selectbox("Output language", LANGUAGES)
file = st.file_uploader("Upload a PDF, TXT, or image", type=[
                        "pdf", "txt", "png", "jpg", "jpeg"])
text = st.text_area("Or paste text here", height=250)

is_image = bool(file) and file.type.startswith("image/")

if file and not is_image:
    try:
        if file.name.lower().endswith(".pdf"):
            text = read_pdf(file)
        else:
            text = file.read().decode("utf-8")
    except Exception as e:
        text = ""
        st.error(f"Could not read the file: {e}")

if is_image:
    st.image(file, caption="Uploaded image")

if st.button("Summarize"):
    try:
        with st.spinner("Summarizing..."):
            if is_image:
                result = summarize_image(
                    file.getvalue(), file.type, style, language)
            else:
                result = summarize(text, style, language)
        st.subheader("Summary")
        st.write(result)
    except Exception as e:
        st.error(str(e))
