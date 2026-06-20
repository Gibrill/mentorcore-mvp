import streamlit as st
import os
import requests
import json
import urllib.parse
import time

# 1. Configurare pagină
st.set_page_config(page_title="MentorCore B2B", page_icon="🧠")
st.title("MentorCore 🧠")
st.subheader("Asistent Operațional B2B")

# 2. Setări
api_key = os.environ.get("GEMINI_API_KEY")
user_input = st.text_area("Ce rezolvăm astăzi?", placeholder="Ex: Programează ședință cu Vasile la ora 19:00", height=100)

# 3. Logica principală
if st.button("Procesează"):
    if api_key and user_input:
        # URL-ul corect pentru modelul detectat în contul tău
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        
        # Prompt definit riguros pentru a forța formatul corect de dată
        prompt = f"""Ești un asistent B2B. Extrage informații pentru un eveniment din textul: '{user_input}'.
        Returnează DOAR un obiect JSON valid, fără alt text: 
        {{ "intent": "calendar_event", "title": "...", "start_date": "YYYY-MM-DDTHH:MM:SS" }}
        Exemplu de dată: 2026-06-21T19:00:00"""
        
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        
        with st.spinner("Procesez..."):
            try:
                response = requests.post(url, headers=headers, json=data)
                
                # Gestionare automată limită 429
                if response.status_code == 429:
                    time.sleep(10)
                    response = requests.post(url, headers=headers, json=data)
                
                result = response.json()
                
                if "candidates" in result:
                    raw_text = result["candidates"][0]["content"]["parts"][0]["text"]
                    clean_json = raw_text.replace("```json", "").replace("```", "").strip()
                    json_data = json.loads(clean_json)
                    
                    if json_data.get("intent") == "calendar_event":
                        titlu = urllib.parse.quote(json_data["title"])
                        # Transformare dată pentru Google Calendar (format YYYYMMDDTHHMMSSZ)
                        start = json_data["start_date"].replace("-", "").replace(":", "").replace("T", "") + "Z"
                        link = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={titlu}&dates={start}/{start}"
                        
                        st.success("Eveniment pregătit!")
                        st.markdown(f'<a href="{link}" target="_blank" style="display:inline-block; padding:12px 24px; background:#4285F4; color:white; text-decoration:none; border-radius:6px; font-weight:bold;">📅 Adaugă în Google Calendar</a>', unsafe_allow_html=True)
                    else:
                        st.write("Rezultat:", raw_text)
                else:
                    st.error(f"Eroare API: {result}")
            except Exception as e:
                st.error(f"Eroare procesare: {e}")
    else:
        st.error("Cheia API lipsește sau input gol.")
