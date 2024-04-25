import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from PyPDF2 import PdfReader
import os

os.environ['LANGCHAIN_API_KEY'] = "ls__5292f139587b42e4a2be8f9f374ddced"
os.environ['GOOGLE_API_KEY'] = "AIzaSyDXInMq_3VVc96niTrRjp2RLpWFhl_09mY"
os.environ['LANGCHAIN_TRACING_V2'] = 'True'

prompt = ChatPromptTemplate.from_messages(
    [
        ('system', """
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{resume}
description:{description}

I want the response as per below structure
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
"""),
        ('user' , 'analyze my resume and provide matching score')
    ]
)

llm = ChatGoogleGenerativeAI(model='gemini-pro')
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

st.title('Resume Shortlister')
upload_files = st.file_uploader('Upload resumes', type='pdf', accept_multiple_files=True)

job_description = st.text_input('Enter job description')

if job_description:
    for cv in upload_files:
        st.write(cv.name)
        extracted_text = ''

        pdf = PdfReader(cv)
        for page_num in range(len(pdf.pages)):
                page = pdf.pages[page_num]
                extracted_text += page.extract_text()
        print(extracted_text)
        st.write(chain.invoke({'description': job_description, 'resume': extracted_text}))
