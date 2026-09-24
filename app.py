import streamlit as st

from src.processor import process_vtt
from src.file_handler import save_notes


st.set_page_config(
    page_title="VTT Notes Generator",
    page_icon="📝"
)

st.title("VTT → Study Notes")

uploaded_file = st.file_uploader(
    "Upload VTT file",
    type=["vtt"]
)

if st.button("Submit", type="primary"):

    if uploaded_file is None:
        st.warning("Please upload a VTT file.")
        st.stop()

    with st.spinner("Processing transcript..."):

        vtt_text = uploaded_file.read().decode(
            "utf-8",
            errors="ignore"
        )

        final_notes = process_vtt(vtt_text)

    st.success("Notes generated successfully.")

    st.download_button(
        label="Download Notes",
        data=final_notes,
        file_name=uploaded_file.name.replace(".vtt", ".txt"),
        mime="text/plain"
    )