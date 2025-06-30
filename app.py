import streamlit as st
import pdfplumber
import graphviz
import re

st.set_page_config(layout="wide")
st.title("📘 Disleksi Dostu Zihin Haritası Uygulaması")

uploaded_file = st.file_uploader("PDF dosyanızı yükleyin", type=["pdf"])

if uploaded_file:
    full_text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text

    if full_text.strip() == "":
        st.warning("PDF'den metin çıkarılamadı. Lütfen farklı bir dosya deneyin.")
    else:
        st.subheader("📖 Çıkarılan Metin (İlk 800 karakter)")
        st.write(full_text[:800] + ("..." if len(full_text) > 800 else ""))

        # Satırlara böl ve başlık benzeri ifadeleri topla
        lines = full_text.split("\n")
        keywords = [line.strip() for line in lines if 4 < len(line.strip()) < 80]
        headings = [line for line in keywords if line.istitle() or line.isupper()]
        headings = list(dict.fromkeys(headings))[:10]  # ilk 10 başlık

        if headings:
            st.subheader("🧠 Zihin Haritası")

            dot = graphviz.Digraph()
            dot.node("Konu", shape="oval", color="deepskyblue", style="filled", fontname="Arial")

            for i, h in enumerate(headings):
                node_id = f"alt{i}"
                dot.node(node_id, h, shape="box", color="lightgreen", style="filled", fontname="Arial")
                dot.edge("Konu", node_id)

            st.graphviz_chart(dot, use_container_width=True)
        else:
            st.warning("Metinde yeterli başlık yapısı bulunamadı.")

else:
    st.info("Lütfen yukarıdan bir PDF dosyası yükleyin.")
