import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()  # Load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, resume_text, jd_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input.format(text=resume_text, jd=jd_text))
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Templates
input_prompt1 = """
You are an experienced Technical Human Resource Manager, and your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
resume:{text}
description:{jd}
"""

input_prompt2 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description and suggest ways to improve the skills. 
Provide feedback on how the applicant can enhance their skills to match the job requirements.
resume:{text}
description:{jd}
"""

input_prompt3 = """
You are an experienced hiring manager for a tech company. Your task is to evaluate the resume and assign a percentage match 
based on the provided job description. Also, list the missing keywords with high accuracy and provide final thoughts on the profile.
resume:{text}
description:{jd}
"""

def display_upload_ui():
    # st.sidebar.image("https://img.icons8.com/ios/452/resume.png", width=100)
    st.title("Smart ATS")
    st.text("Improve Your Resume ATS")
    jd = st.text_area("Paste the Job Description")
    uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", help="Please upload the PDF file")
    return jd, uploaded_file

def display_response(response):
    st.subheader("AI Evaluation Result:")
    st.success(response)

def display_error(message):
    st.subheader("Error:")
    st.error(message)

def main():
    jd, uploaded_file = display_upload_ui()

    submit1 = st.button("Submit 1: Evaluate Profile Alignment")
    submit2 = st.button("Submit 2: Improve Skills Feedback")
    submit3 = st.button("Submit 3: Percentage Match and Missing Keywords")

    if submit1:
        if uploaded_file is not None:
            try:
                resume_text = input_pdf_text(uploaded_file)
                response = get_gemini_response(input_prompt1, resume_text, jd)
                display_response(response)
            except Exception as e:
                display_error(f"Error processing the file: {str(e)}")
        else:
            display_error("Please upload a resume file.")

    elif submit2:
        if uploaded_file is not None:
            try:
                resume_text = input_pdf_text(uploaded_file)
                response = get_gemini_response(input_prompt2, resume_text, jd)
                display_response(response)
            except Exception as e:
                display_error(f"Error processing the file: {str(e)}")
        else:
            display_error("Please upload a resume file.")

    elif submit3:
        if uploaded_file is not None:
            try:
                resume_text = input_pdf_text(uploaded_file)
                response = get_gemini_response(input_prompt3, resume_text, jd)
                display_response(response)
            except Exception as e:
                display_error(f"Error processing the file: {str(e)}")
        else:
            display_error("Please upload a resume file.")

if __name__ == "__main__":
    main()
