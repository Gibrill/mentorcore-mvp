import streamlit as st
import os
import requests

st.set_page_config(page_title="MentorCore B2B", page_icon="🧠")
st.title("MentorCore 🧠")

api_key = os.environ.get("GEMINI_API_KEY")
user_input = st.text_area("Ce rezolvăm astăzi?")

if st.button("Procesează"):
    if api_key and user_input:
        # URL-ul stabil
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        # Consolidăm instrucțiunile direct în text (fără campuri JSON externe care dau eroare)
        prompt_final = f"""ROL: MentorCore asistent B2B.
        REGULI: 
        1. PROGRAMARE: JSON valid {{ "intent": "calendar_event", "title": "...", "start_date": "...", "duration_minutes": 60 }}
        2. MARKETING: Format cu ### LINKEDIN, ### NEWSLETTER, ### REZUMAT INTERN.
        
        INPUT UTILIZATOR: {user_input}"""
        
        data = {"contents": [{"parts": [{"text": prompt_final}]}]}
        
        try:
            response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
            result = response.json()
            
            if "candidates" in result:
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                st.markdown(text)
            else:
                st.error(f"Eroare API: {result}")
        except Exception as e:
            st.error(f"Eroare: {e}")
