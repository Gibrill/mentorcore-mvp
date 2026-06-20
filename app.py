import streamlit as st
import google.generativeai as genai
import os

st.title("Diagnostic API")
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

try:
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_methods]
    st.write("Modele disponibile în contul tău:")
    st.write(models)
except Exception as e:
    st.error(f"Eroare la listarea modelelor: {e}")
