import streamlit as st
import requests
import streamlit_authenticator as stauth
import json
import os

# --- 1. CONFIGURAZIONE DATI (METTI I TUOI QUI) ---
# Esempio: se il tuo link è ://github.com, USER è "mario" e REPO è "anime-web"
USER = "IL_TUO_NOME_UTENTE_GITHUB" theadmin
REPO = "IL_NOME_DELLA_TUA_REPOSITORY"anime-web

URL_SFONDO = f"https://githubusercontent.com{USER}/{REPO}/main/sfondo.jpg"
URL_BENVENUTO = f"https://githubusercontent.com{USER}/{REPO}/main/benvenuto.jpg"

# --- 2. STILE E TRASPARENZA ---
st.set_page_config(page_title="Re:Zero Portal", layout="wide")

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{URL_SFONDO}");
        background-size: cover;
        background-attachment: fixed;
    }}
    /* Rimuove i blocchi neri per far vedere lo sfondo */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMainViewContainer"] {{
        background-color: rgba(0, 0, 0, 0) !important;
    }}
    .main .block-container {{
        background-color: rgba(30, 0, 50, 0.8);
        border-radius: 20px;
        padding: 40px;
        border: 2px solid #a020f0;
    }}
    .logo-text {{
        font-size: 38px !important;
        font-weight: 900;
        color: #a020f0 !important;
        text-align: center;
        text-shadow: 2px 2px 10px #fff;
    }}
    .anime-card {{
        background-color: white;
        border-radius: 15px;
        padding: 15px;
        color: #000 !important;
        border: 2px solid #a020f0;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SISTEMA ACCOUNT ---
if 'users' not in st.session_state:
    st.session_state['users'] = {"usernames": {"admin": {"name": "Subaru", "password": "123", "email": "lugnica@news.it"}}}

authenticator = stauth.Authenticate(st.session_state['users'], "rezero_key", "sig", cookie_expiry_days=30)
st.sidebar.markdown('<p class="logo-text">🦋<br>RE:ZERO INFO</p>', unsafe_allow_html=True)
authenticator.login(location='sidebar')
auth_status = st.session_state.get('authentication_status')

# --- 4. CONTENUTO ---
if auth_status:
    st.sidebar.success(f"Benvenuto, {st.session_state.get('name')}")
    authenticator.logout('Logout', 'sidebar')
    st.title("❄️ RE:ZERO KNOWLEDGE BASE")
    
    # Caricamento personaggi Re:Zero (ID: 31240)
    try:
        res = requests.get("https://jikan.moe").json().get('data', [])[:6]
        cols = st.columns(3)
        for i, item in enumerate(res):
            char = item['character']
            with cols[i % 3]:
                st.markdown(f'<div class="anime-card"><img src="{char["images"]["jpg"]["image_url"]}" style="width:100%; height:250px; object-fit:cover; border-radius:10px;"><h4 style="color:black;">{char["name"]}</h4><p style="color:purple;">{item["role"]}</p></div>', unsafe_allow_html=True)
    except:
        st.error("Errore API")

else:
    st.title("🏯 ACCEDI AL PORTALE DI LUGNICA")
    # Carica l'immagine di benvenuto direttamente dal tuo GitHub
    st.image(URL_BENVENUTO, use_container_width=True)
    
    with st.sidebar.expander("🆕 REGISTRATI"):
        try:
            if authenticator.register_user(location='sidebar'):
                st.success('Registrato!')
        except Exception as e:
            st.error(f"Errore: {e}")
