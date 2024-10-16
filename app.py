import streamlit as st
import requests
import pandas as pd

# Backend API endpoint (Update this with your backend URL)
BACKEND_API_URL = "http://127.0.0.1:8000/rank-resumes"

st.set_page_config(page_title="Resume Ranking System", layout="wide")

st.title("AI-Powered Resume Ranking System")
st.write("Upload a job description and multiple resumes to get ranked results.")

# Upload Job Description
st.header("Step 1: Upload Job Description")
jd_file = st.file_uploader("Upload JD as a text file", type=["txt", "pdf"])
jd_text = st.text_area("Or paste Job Description here", height=150)

if jd_file:
    jd_text = jd_file.read().decode("utf-8")

st.header("Step 2: Upload Resumes")
uploaded_resumes = st.file_uploader(
    "Upload one or more resumes (PDF/Text)", type=["pdf", "txt"], accept_multiple_files=True
)

if st.button("Rank Resumes"):
    if not jd_text or not uploaded_resumes:
        st.error("Please upload both a job description and at least one resume.")
    else:
        resumes_data = [
            {"filename": resume.name, "content": resume.read().decode("utf-8")}
            for resume in uploaded_resumes
        ]

        payload = {"job_description": jd_text, "resumes": resumes_data}

        with st.spinner("Ranking resumes..."):
            try:
                response = requests.post(BACKEND_API_URL, json=payload)
                if response.status_code == 200:
                    ranked_resumes = response.json()["ranked_resumes"]
                    st.success("Resumes ranked successfully!")
                    df = pd.DataFrame(ranked_resumes)
                    st.table(df)
                else:
                    st.error("Failed to rank resumes. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
