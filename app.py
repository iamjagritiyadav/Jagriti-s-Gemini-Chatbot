import streamlit as st
import google.generativeai as genai

# Streamlit secrets se API key uthana
api_key = st.secrets["GOOGLE_API_KEY"]

# Gemini model configure karna
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

# App ka Title
st.title("Jagriti's Gemini Chatbot")

# User se input lena
user_input = st.text_input("You: ", "")

# Agar user ne kuch likha hai toh response generate karna
if st.button("Send"):
    if user_input:
        response = model.generate_content(user_input)
        st.write("Gemini: ", response.text)
    else:
        st.write("Please enter a prompt.")
