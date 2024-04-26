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
        ('system', """you are an AI application Tracking System having lots of knowledge in hiring procees and expert in finding how much does a resume suit to a particular job description , you read evaluate and analyse the resume data provided to you by the user and provide him with matching score in percentage"""),
        ('user' , '''analyze my resume and provide matching score , 
         here is my resume data :{resume}
         this is the job description with which you should compare my resume data and provide matching score : {description}
         
         provide the output in following structure as shown in the below example:

         {{ matching score : 82%
            reason : The skills and projects doesnt match the requirements in provided job description}}

            Follow the above structure and see that the reason is clear and short
         '''
         
         )
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
