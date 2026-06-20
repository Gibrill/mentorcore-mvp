import os
import json
import urllib.parse
import streamlit as st
import google.generativeai as genai

# 1. Configurare UI
st.set_page_config(page_title="MentorCore B2B", page_icon="🧠", layout="centered")
st.title("MentorCore 🧠")
st.subheader("Asistent Operațional B2B")

# 2. Configurare Model
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""ROL: Ești 'MentorCore', asistent B2B strict operațional. Nu oferi salutări sau explicații. Returnezi exclusiv output determinist.
REGULI:
1. PROGRAMARE: JSON valid { "intent": "calendar_event", "title": "...", "start_date": "YYYY-MM-DDTHH:MM:SS", "duration_minutes": 60 }
2. MARKETING: Format cu delimitatori ### LINKEDIN, ### NEWSLETTER, ### REZUMAT INTERN."""
)

# 3. Interfață
user_input = st.text_area("Ce rezolvăm astăzi?", placeholder="Ex: Programează ședință cu Mihai vineri 15:00...", height=100)

if st.button("Procesează Intenția", type="primary"):
    if user_input:
        with st.spinner("Procesez..."):
            try:
                # Apelul modelului
                response = model.generate_content(user_input)
                raw = response.text.strip()

                # 4. Procesarea output-ului
                if raw.startswith("{") and "calendar_event" in raw:
                    data = json.loads(raw)
                    titlu = urllib.parse.quote(data["title"])
                    start = data["start_date"].replace("-", "").replace(":", "").replace("T", "")
                    link = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={titlu}&dates={start}Z/{start}Z"
                    
                    st.success("Eveniment pregătit!")
                    st.markdown(f'<a href="{link}" target="_blank" style="display:block; text-align:center; padding:15px; background:#4CAF50; color:white; font-weight:bold; border-radius:8px; text-decoration:none;">📅 Adaugă în Calendar</a>', unsafe_allow_html=True)
                else:
                    st.success("Conținut generat cu succes!")
                    st.markdown(raw)
            except Exception as e:
                st.error(f"Eroare: {e}")
    else:
        st.warning("Introdu o comandă validă.")
