import streamlit as st
import os
import requests
import time

# 1. Configurare pagină
st.set_page_config(page_title="MentorCore B2B", page_icon="🧠")
st.title("MentorCore 🧠")
st.subheader("Asistent Operațional B2B")

# 2. Setări cheie
api_key = os.environ.get("GEMINI_API_KEY")
user_input = st.text_area("Ce rezolvăm astăzi?", placeholder="Ex: Programează ședință...", height=100)

# 3. Logica de procesare
if st.button("Procesează"):
    if api_key and user_input:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": f"ROL: MentorCore asistent B2B strict operațional. REGULI: 1. PROGRAMARE: JSON valid {{ 'intent': 'calendar_event', 'title': '...', 'start_date': 'YYYY-MM-DDTHH:MM:SS', 'duration_minutes': 60 }}. 2. MARKETING: Format cu ### LINKEDIN, ### NEWSLETTER, ### REZUMAT INTERN. INPUT: {user_input}"}]}]}
        
        with st.spinner("Procesez prin API..."):
            try:
                response = requests.post(url, headers=headers, json=data)
                
                # Gestionare eroare 429 (Rate Limit)
                if response.status_code == 429:
                    st.warning("Limită atinsă, reîncerc automat în 10 secunde...")
                    time.sleep(10)
                    response = requests.post(url, headers=headers, json=data)
                
                result = response.json()
                
                if "candidates" in result:
                    text = result["candidates"][0]["content"]["parts"][0]["text"]
                    st.markdown(text)
                else:
                    st.error(f"Eroare API: {result}")
                    
            except Exception as e:
                st.error(f"Eroare sistem: {e}")
    else:
        st.error("Cheie API lipsă sau input gol.")
