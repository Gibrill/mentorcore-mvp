import streamlit as st
import os
import requests
import json
import urllib.parse
import time
from datetime import datetime

st.set_page_config(page_title="MentorCore B2B", page_icon="🧠")
st.title("MentorCore 🧠")

api_key = os.environ.get("GEMINI_API_KEY")
user_input = st.text_area("Ce rezolvăm astăzi?", placeholder="Ex: Ședință cu Vasile mâine la ora 19:00")

if st.button("Procesează"):
    if api_key and user_input:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
        
        # Am simplificat promptul pentru a fi 100% sigur pe formatul datei
        prompt = f"Extrage datele pentru calendar din: '{user_input}'. Returnează DOAR JSON: {{ 'title': 'Titlu', 'start_date': 'YYYY-MM-DDTHH:MM:SS' }}. Folosește data curentă 2026-06-20 dacă nu e specificată."
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        
        with st.spinner("Procesez..."):
            try:
                response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
                if response.status_code == 429:
                    time.sleep(5)
                    response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
                
                result = response.json()
                raw_text = result["candidates"][0]["content"]["parts"][0]["text"].replace("```json", "").replace("```", "").strip()
                json_data = json.loads(raw_text)
                
                # Procesare link cu formatare strictă
                titlu = urllib.parse.quote(json_data.get("title", "Eveniment"))
                
                # Forțăm formatul pentru link: YYYYMMDDTHHMMSS
                data_dt = datetime.fromisoformat(json_data["start_date"])
                start_str = data_dt.strftime("%Y%m%dT%H%M%S")
                
                link = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={titlu}&dates={start_str}/{start_str}"
                
                st.success(f"Programat: {json_data['title']} la {json_data['start_date']}")
                st.markdown(f'<a href="{link}" target="_blank" style="display:inline-block; padding:12px 24px; background:#4285F4; color:white; text-decoration:none; border-radius:6px; font-weight:bold;">📅 Adaugă în Google Calendar</a>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Eroare: {e}. Asigură-te că data este în format complet.")
    else:
        st.error("Cheie API lipsă sau input gol.")
