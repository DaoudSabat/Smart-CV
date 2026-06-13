"""Streamlit entry point for SmartCV."""
import os

import streamlit as st
from dotenv import load_dotenv

from core.cv_generator import CVGenerator
from core.template_renderer import TemplateRenderer

load_dotenv()

if "cv_file" not in st.session_state:
    st.session_state["cv_file"] = ""

st.set_page_config(page_title="SmartCV", page_icon="💼")
st.title("SmartCV – GPT-based CV Generator")
st.markdown("Generate a professional one-page resume from your real experience.")

selected_template = st.radio("Choose a CV template:", ["default", "modern", "classic"], horizontal=True)

st.header("Personal Info")
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone")
address = st.text_input("Address")
job_title = st.text_input("Target Job Title")
linkedin = st.text_input("LinkedIn URL (optional)")

st.header("Background")
skills = st.text_area("Technical skills")
experience = st.text_area("Work experience summary")
projects = st.text_area("Best projects")
education = st.text_area("Education")

st.header("Languages")
language_entries = []
language_count = st.number_input("How many languages?", min_value=1, max_value=10, value=1)
for i in range(language_count):
    lang = st.selectbox(
        f"Language #{i+1}",
        ["English", "Arabic", "French", "Spanish", "German", "Hebrew",
         "Chinese", "Russian", "Hindi", "Other"],
        key=f"lang_{i}",
    )
    proficiency = st.selectbox(
        f"Proficiency in {lang}",
        ["Basic", "Conversational", "Fluent", "Native"],
        key=f"prof_{i}",
    )
    language_entries.append(f"{lang} - {proficiency}")

if st.button("Generate CV"):
    if not name or not email or not job_title or not skills:
        st.warning("Name, email, job title, and skills are required.")
    else:
        with st.spinner("Generating CV using AI..."):
            try:
                generator = CVGenerator()
                sections = generator.generate({
                    "name": name, "email": email, "phone": phone,
                    "address": address, "linkedin": linkedin,
                    "job_title": job_title, "skills": skills,
                    "experience": experience, "projects": projects,
                    "education": education, "languages": language_entries,
                })
                renderer = TemplateRenderer(selected_template)
                pdf_path = renderer.render_cv(sections)
                st.session_state["cv_file"] = pdf_path
                st.success("CV Generated Successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

if st.session_state["cv_file"]:
    with open(st.session_state["cv_file"], "rb") as f:
        st.download_button("Download CV PDF", f, file_name="SmartCV.pdf", mime="application/pdf")
