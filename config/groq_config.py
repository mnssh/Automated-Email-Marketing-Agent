import streamlit as st
from groq import Groq

def get_groq_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])
