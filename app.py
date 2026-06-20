import streamlit as st
import os
import requests
import json
import urllib.parse
import time

st.set_page_config(page_title="MentorCore B2B", page_icon="🧠")
st.title("MentorCore 🧠")
st.subheader("Asistent Operațional B2B")

api_key = os.environ.get("GEMINI_API_KEY")
user_input = st.text_area("Ce rezolvăm astăzi?", placeholder="Ex: Programează ședință cu Vasile la 19:00", height=100)

if st.button("Procesează"):
    if api_key and user_input:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        prompt = f"Ești asistent B2B. Extrage din: '{user_input}'. Returnează DOAR JSON valid: {{ 'intent': 'calendar_event', 'title': '...', 'start_date': 'YYYY-MM-DDTHH:MM:SS' }}."
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        
        with st.spinner("Procesez..."):
            try:
                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 429:
                    time.sleep(10)
                    response = requests.post(url, headers=headers, json=data)
                
                result = response.json()
                raw_text = result["candidates"][0]["content"]["parts"][0]["text"].replace("```json", "").replace("```", "").strip()
                json_data = json.loads(raw_text)
                
                if json_data.get("intent") == "calendar_event":
                    titlu = urllib.parse.quote(json_data["title"])
                    start = json_data["start_date"].replace("-", "").replace(":", "").replace("T", "") + "Z"
                    link = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={titlu}&dates={start}/{start}"
                    st.success("Eveniment pregătit!")
                    st.markdown(f'<a href="{link}" target="_blank" style="display:inline-block; padding:12px 24px; background:#4285F4; color:white; text-decoration:none; border-radius:6px; font-weight:bold;">📅 Adaugă în Google Calendar</a>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Eroare: {e}")
