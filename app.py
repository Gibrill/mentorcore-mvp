import streamlit as st
import os
import requests
import json
import urllib.parse
import time

# 1. Configurare pagină
st.set_page_config(page_title="MentorCore B2B", page_icon="🧠")
st.title("MentorCore 🧠")

api_key = os.environ.get("GEMINI_API_KEY")
user_input = st.text_area("Ce rezolvăm astăzi?", placeholder="Ex: Programează ședință...")

if st.button("Procesează"):
    if api_key and user_input:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        # Cerem explicit JSON pentru procesare
        data = {"contents": [{"parts": [{"text": f"ROL: MentorCore asistent B2B. Extrage JSON valid {{ 'intent': 'calendar_event', 'title': '...', 'start_date': 'YYYY-MM-DDTHH:MM:SS', 'duration_minutes': 60 }}. Nu afișa nimic altceva în afară de JSON. INPUT: {user_input}"}]}]}
        
        with st.spinner("Procesez..."):
            try:
                response = requests.post(url, headers=headers, json=data)
                result = response.json()
                
                if "candidates" in result:
                    raw_text = result["candidates"][0]["content"]["parts"][0]["text"]
                    # Curățăm textul de markdown-ul de tip cod (```json ... ```)
                    clean_json = raw_text.replace("```json", "").replace("```", "").strip()
                    json_data = json.loads(clean_json)
                    
                    if json_data.get("intent") == "calendar_event":
                        titlu = urllib.parse.quote(json_data["title"])
                        start = json_data["start_date"].replace("-", "").replace(":", "").replace("T", "")
                        link = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={titlu}&dates={start}Z/{start}Z"
                        
                        st.success("Eveniment pregătit!")
                        st.markdown(f'<a href="{link}" target="_blank" style="display:inline-block; padding:10px 20px; background:#4285F4; color:white; text-decoration:none; border-radius:5px; font-weight:bold;">📅 Adaugă în Google Calendar</a>', unsafe_allow_html=True)
                    else:
                        st.markdown(raw_text)
                else:
                    st.error("Eroare API.")
            except Exception as e:
                st.error("Se procesează... te rog apasă din nou dacă durează.")
    else:
        st.error("Cheie API lipsă!")
