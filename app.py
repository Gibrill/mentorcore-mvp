import os
import json
import urllib.parse
import streamlit as st
from google import genai
from google.genai import types

# 1. Configurarea interfeței (Cum va arăta pe ecran)
st.set_page_config(page_title="MentorCore B2B", page_icon="🧠", layout="centered")
st.title("MentorCore 🧠")
st.subheader("Asistent Operațional B2B")

# Preluăm cheia API (Asigură-te că o ai setată în terminal sau lipește-o aici pentru test)
api_key = os.environ.get("GEMINI_API_KEY") 
client = genai.Client(api_key=api_key)

# 2. Zona de Input pentru utilizator
user_input = st.text_area("Ce rezolvăm astăzi?", placeholder="Ex: Programează o ședință cu Mihai vineri la 15:00...", height=100)

# 3. Logica de Execuție (Butonul)
if st.button("Procesează Intenția", type="primary"):
    if user_input:
        with st.spinner("Analizez și generez structura..."):
            try:
                # Aici este exact "creierul" pe care l-am setat în AI Studio
                generate_content_config = types.GenerateContentConfig(
                    max_output_tokens=2000,
                    temperature=0.0,
                    top_p=0.0,
                    system_instruction=[
                        types.Part.from_text(text="""ROL: 
Ești "MentorCore", un asistent AI B2B strict operațional, integrat într-o aplicație mobilă dedicată mentorilor și experților în consultanță. Scopul tău este procesarea deterministă a intențiilor utilizatorului. Nu ești un chatbot conversațional. Nu oferi salutări, scuze sau explicații. Returnezi exclusiv output formatat conform regulilor de mai jos.

REGULI DE PROCESARE A INTENȚIEI (ROUTING LOGIC):
Analizează inputul utilizatorului și încadrează-l în una dintre cele 3 categorii. Execută doar acțiunea aferentă categoriei detectate.

1. INTENȚIA: PROGRAMARE CALENDAR
- Acțiune: Extrage detaliile evenimentului. Dacă durata nu este specificată, asociază implicit 60 de minute.
- Regula de Output: Returnează EXCLUSIV un obiect JSON valid, fără formatare Markdown.
- Structura JSON obligatorie: 
{
  "intent": "calendar_event",
  "title": "[Numele sau scopul întâlnirii]",
  "start_date": "[Data estimată în format ISO 8601]",
  "duration_minutes": [Număr întreg]
}

2. INTENȚIA: REAMINTIRE SUBSCRIPȚIE
- Acțiune: Redactează un draft de mesaj profesional, politicos, orientat spre B2B.
- Regula de Output: Returnează EXCLUSIV textul mesajului.

3. INTENȚIA: GENERARE MARKETING / REZUMAT
- Acțiune: Formatează inputul în 3 tipuri de conținut distinct.
- Regula de Output: Respectă exact această structură cu delimitatori:
### LINKEDIN
[Postare profesională...]
---
### NEWSLETTER
[Email scurt...]
---
### REZUMAT INTERN
[3 puncte extrase...]""")
                    ],
                )

                # Apelul către AI
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=user_input,
                    config=generate_content_config,
                )
                
                # 4. Afișarea rezultatului pe ecran (Ascuns pentru client)
                raw_response = response.text.strip()

                # Verificăm dacă AI-ul a returnat un JSON pentru calendar
                if raw_response.startswith("{") and "calendar_event" in raw_response:
                    try:
                        # Parsăm datele în fundal
                        date_json = json.loads(raw_response)
                        titlu_codat = urllib.parse.quote(date_json["title"])
                        # Formatăm data pentru Google Calendar (fără cratime)
                        data_start = date_json["start_date"].replace("-", "").replace(":", "")
                        
                        # Generăm link-ul universal
                        link_calendar = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={titlu_codat}&dates={data_start}Z/{data_start}Z"
                        
                        st.success("Datele evenimentului au fost extrase!")
                        # Afișăm doar un buton vizual HTML, nu JSON-ul
                        st.markdown(f'<a href="{link_calendar}" target="_blank" style="display: block; text-align: center; padding: 15px; background-color: #4CAF50; color: white; font-weight: bold; text-decoration: none; border-radius: 8px;">📅 Salvează în Google Calendar</a>', unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.error("Sistemul a întâmpinat o problemă la asamblarea calendarului.")
                else:
                    # Dacă intenția a fost Generare Marketing sau Reamintire Subscripție
                    # Afișăm textul curat generat de AI
                    st.success("Conținut generat cu succes!")
                    st.markdown(raw_response)

            except Exception as e:
                st.error(f"Eroare de sistem: {e}")
    else:
        st.warning("Te rog introdu o comandă validă înainte de a apăsa butonul.")