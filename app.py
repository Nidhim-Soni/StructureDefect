import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import datetime as dt

# Lets configure the model

gemini_api_key = os.getenv('Google_API_Key2')
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# lets create sidebar for image uplaod 

st.sidebar.title(':red[Upload the Images Here: ]')
uploaded_image = st.sidebar.file_uploader('Image',type=['jpeg','jpg','png','jfif'])
if uploaded_image:
    uploaded_image = Image.open(uploaded_image)
    st.sidebar.success('Images has been loaded successfully')
    st.sidebar.subheader(':blue[Uploaded Images]')
    st.sidebar.image(uploaded_image)

# Lets create the main Page

st.title(':orange[STRUCTURAL DEFECT DETECTION :-] :blue[🧱 Structural Defect Detection & Smart Reporting (AI)]')
st.markdown('#### :green[This application takes the images of the structural defect from the construction site and prepare the AI assisted report.]')
title=st.text_input('Enter the Title of the report: ')
name=st.text_input('Enter the Name of the person who has prepared input: ')
desig=st.text_input('Enter the designation of person who have prepared the report: ')
org=st.text_input('Enter the name of the organisation: ')

if st.button('SUBMIT'):
    with st.spinner('Processing....'):
        prompt = f'''
                <Role> You are an expert structural engineer with 20+ years of experience in construction
                <Goal> You need to prepare a detailed report on the structural defect shown in the images provided by the user.
                <Context> the images shared by the user has been attached
                <Format> Follow the steps to prepare the report
                * Add title at the top of the report. The title provided by the user is {title}.
                * next add name ,designation and organization of the person who has prepared the report. Also include the date.Following are the details 
                provided by the user
                    name : {name}
                    designation : {desig}
                    organisation : {org}
                    date : {dt.datetime.now().date()}
                * Identify and classify the defect for eg. crack, spalling,corossion,honey combining
                * There could be more than one defects in images. Identify all defects separately
                * For each defect highlighted or identified provide a short description of the defects and its potential imapact on the structure
                * For each defect measure the severity as low, medium, or high. Also Mention if the defect is inevitable or avoidable
                * Provide the short term and long term solution for the repair along with an estimated cost in INR along with the estimated time
                * What precautionary measure can be taken to avoid these measures in the future.
                <Instruction> * The report generated should be in word Format.
                * Dont use HTML Commands or codes
                * Use Bullets points and tabular form where ever possible.
                * Make sure the report does not exceed 3 pages.
                * Make the report look formal and attractive.
                * the format of the report should not be informal and alligns to the latest format of report writing.
            '''
        response = model.generate_content([prompt,uploaded_image],
                                          generation_config={'temperature':0.9})
        st.write(response.text)

        if st.download_button(
            label='Click To Download',
            data=response.text,
            file_name='Structural_defect_report.txt',
            mime='text/plain'
        ):
            st.success('The File is Downloaded Successfully')