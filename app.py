import streamlit as st
import tempfile
from model import detect_languages


st.set_page_config(page_title="Multi-Language Detector", layout="wide")

st.title("📘 Multi-Language Detection From Image")
st.write("Upload an image and the system will detect all languages present and calculate percentage distribution.")

uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(uploaded_file.read())
    img_path = temp.name

    
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    st.info("⏳ Detecting languages... Please wait.")

    result = detect_languages(img_path)

    if "error" in result:
        st.error(result["error"])
    else:
        st.success(f"🏆 Dominant Language: **{result['dominant_language']}** ({result['dominant_percentage']}%)")

        st.subheader("📊 Language Percentage Distribution")
        st.write(result["percentages"])

        st.subheader("📝 Extracted Text")
        st.text_area("", value=result["extracted_text"], height=300)
