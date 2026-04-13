import streamlit as st
import requests
import streamlit_authenticator as stauth
import json
import os
from datetime import datetime

# --- 1. CONFIGURAZIONE E STILE (Sfondo Manga + Trasparenza) ---
st.set_page_config(page_title="My Anime News", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    /* SFONDO MANGA (Vignette) */
    .stApp {
        background-image: url("https://imgur.com");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }

    /* TRASPARENZA TOTALE (Elimina il nero che copre lo sfondo) */
    [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"], 
    [data-testid="stMainViewContainer"] {
        background-color: rgba(0, 0, 0, 0) !important;
    }

    /* VELO SCURO centrato per rendere leggibile il testo */
    .main .block-container {
        background-color: rgba(0, 0, 0, 0.75);
        border-radius: 20px;
        padding: 40px;
        margin-top: 20px;
        border: 1px solid rgba(255, 75, 75, 0.3);
    }
    
    /* LOGO NELLA SIDEBAR */
    .logo-text {
        font-size: 42px !important;
        font-weight: 900;
        color: #ff4b4b !important;
        text-align: center;
        text-shadow: 2px 2px 10px #000;
    }

    /* CARD ANIME */
    .anime-card {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 15px;
        color: #000 !important;
        border: 2px solid #ff4b4b;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SISTEMA ACCOUNT ---
if 'users' not in st.session_state:
    st.session_state['users'] = {"usernames": {"admin": {"name": "Admin", "password": "123", "email": "a@a.it"}}}

authenticator = stauth.Authenticate(st.session_state['users'], "anime_pro_key", "sig_key", cookie_expiry_days=30)
st.sidebar.markdown('<p class="logo-text">🏮<br>MY ANIME NEWS</p>', unsafe_allow_html=True)
authenticator.login(location='sidebar')

auth_status = st.session_state.get('authentication_status')

# --- 3. LOGICA SITO ---
if auth_status:
    name = st.session_state.get('name')
    st.sidebar.success(f"Online: {name}")
    authenticator.logout('Logout', 'sidebar')
    
    st.title("🏮 DATABASE NEWS ATTIVO")
    cat = st.selectbox("CATEGORIA:", ["IN CORSO", "TOP RATED"])
    url = "https://jikan.moe" if cat == "IN CORSO" else "https://jikan.moe"
    
    try:
        data = requests.get(url).json().get('data', [])[:9]
        cols = st.columns(3)
        for i, anime in enumerate(data):
            with cols[i % 3]:
                st.markdown(f'<div class="anime-card"><img src="{anime["images"]["jpg"]["large_image_url"]}" style="width:100%; height:300px; object-fit:cover; border-radius:10px;"><h4 style="color:black; margin-top:10px;">{anime["title"][:25]}</h4></div>', unsafe_allow_html=True)
                st.link_button("SCOPRI DI PIÙ", anime['url'])
    except:
        st.error("Errore nel caricamento dei dati.")

else:
    # --- SCHERMATA DI BENVENUTO CON LA TUA IMMAGINE ---
    st.title("🏯 ACCEDI AL PORTALE")
    
    # Inserimento dell'immagine che hai inviato
    st.image("https://ibb.co", 
             caption="Benvenuto nel Database My Anime News", 
             use_container_width=True)
    
    with st.sidebar.expander("🆕 REGISTRATI"):
        try:
            if authenticator.register_user(location='sidebar', key='reg_form'):
                st.success('Registrato! Accedi sopra.')
        except Exception as e: st.error(f"Errore: {e}")
    
    st.warning("Esegui il login nella barra laterale per entrare nel sistema.")

   
