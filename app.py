import os
import json
import urllib.parse
import streamlit as st
import google.generativeai as genai

# 1. Configurarea interfeței
st.set_page_config(page_title="MentorCore B2B", page_icon="🧠", layout="centered")
st.title("MentorCore 🧠")
st.subheader("Asistent Operațional B2B")

# Configurare Gemini (folosim google-generativeai)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Definire model cu instrucțiunile de sistem incluse
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""ROL: Ești 'MentorCore', un asistent AI B2B strict operațional... (inserează aici tot textul tău lung de system instruction)"""
)

# 2. Zona de Input
user_input = st.text_area("Ce rezolvăm astăzi?", placeholder="Ex: Programează o ședință...", height=100)

# 3. Logica de Execuție
if st.button("Procesează Intenția", type="primary"):
    if user_input:
        with st.spinner("Analizez..."):
            try:
                # Apelul simplificat al modelului
                response = model.generate_content(user_input)
                raw_response = response.text.strip()

                # 4. Procesarea output-ului
                if raw_response.startswith("{") and "calendar_event" in raw_response:
                    date_json = json.loads(raw_response)
                    titlu_codat = urllib.parse.quote(date_json["title"])
                    data_start = date_json["start_date"].replace("-", "").replace(":", "").replace("T", "")
                    
                    link_calendar = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={titlu_codat}&dates={data_start}/{data_start}"
                    
                    st.success("Datele evenimentului au fost extrase!")
                    st.markdown(f'<a href="{link_calendar}" target="_blank" style="display: block; text-align: center; padding: 15px; background-color: #4CAF50; color: white; font-weight: bold; text-decoration: none; border-radius: 8px;">📅 Salvează în Google Calendar</a>', unsafe_allow_html=True)
                
                else:
                    st.success("Conținut generat cu succes!")
                    st.markdown(raw_response)

            except Exception as e:
                st.error(f"Eroare de procesare: {e}")
    else:
        st.warning("Te rog introdu o comandă.")

            except Exception as e:
                st.error(f"Eroare de sistem: {e}")
    else:
        st.warning("Te rog introdu o comandă validă înainte de a apăsa butonul.")
