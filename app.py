import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_to_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""

Evaluate the resume against the provided job description as an experienced Application Tracking System (ATS) with a deep understanding of the tech field, including software engineering, data science, data analysis, and big data engineering. Your task is to assess the resume's relevance to the job market, considering its competitiveness, and provide assistance in improving it. Assign a percentage match based on the job description and identify missing keywords with high accuracy.

Input format:
resume: {text}
description: {jd}

Expected response format:
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}

"""

## streamlit app
st.title("Resume Analysis System")
st.text("Check the Skill Gap Analysis")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_to_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt)
        st.subheader(response)