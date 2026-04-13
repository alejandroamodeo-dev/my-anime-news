import streamlit as st
import requests
import streamlit_authenticator as stauth
import json
import os
from datetime import datetime

# --- 1. CONFIGURAZIONE E DATI GITHUB ---
# Inserisci qui il tuo nome utente e il nome del progetto
USER = "theadmin" 
REPO = "my-anime-news"

URL_SFONDO = f"https://githubusercontent.com{USER}/{REPO}/main/sfondo.jpg"
URL_BENVENUTO = f"https://githubusercontent.com{USER}/{REPO}/main/benvenuto.jpg"

st.set_page_config(page_title="My Anime News Pro", page_icon="🏮", layout="wide")

# --- 2. ANIMAZIONI E STILE CSS ---
st.markdown(f"""
    <style>
    /* ANIMAZIONE ZOOM LENTO SFONDO */
    @keyframes slowZoom {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.1); }}
        100% {{ transform: scale(1); }}
    }}
    
    .stApp {{
        background-image: url("{URL_SFONDO}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        animation: slowZoom 40s infinite ease-in-out;
    }}

    /* TRASPARENZA LIVELLI */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMainViewContainer"] {{
        background-color: rgba(0, 0, 0, 0) !important;
    }}

    /* CONTENITORE CENTRALE */
    .main .block-container {{
        background-color: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(8px);
        border-radius: 20px;
        padding: 40px;
        border: 1px solid rgba(255, 75, 75, 0.4);
        box-shadow: 0 0 30px rgba(255, 75, 75, 0.2);
    }}
    
    /* LOGO GIGANTE ANIMATO */
    @keyframes pulse {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.05); }} 100% {{ transform: scale(1); }} }}
    .logo-text {{
        font-size: 50px !important;
        font-weight: 900;
        color: #ff4b4b !important;
        text-align: center;
        text-shadow: 0 0 15px #ff4b4b;
        animation: pulse 2s infinite;
        line-height: 1.1;
    }}

    /* CARD ANIME */
    .anime-card {{
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #444;
        transition: 0.4s;
    }
    .anime-card:hover {{
        border-color: #ff4b4b;
        transform: translateY(-10px);
        box-shadow: 0 10px 30px rgba(255, 75, 75, 0.4);
    }}
    
    h1, h2, h3 {{ color: #ff4b4b !important; text-shadow: 2px 2px 5px #000; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SISTEMA ACCOUNT ---
if 'users' not in st.session_state:
    st.session_state['users'] = {"usernames": {"admin": {"name": "Admin", "password": "123", "email": "a@a.it"}}}

authenticator = stauth.Authenticate(st.session_state['users'], "anime_pro_key", "sig_key", cookie_expiry_days=30)

st.sidebar.markdown('<p class="logo-text">🏮<br>MY ANIME NEWS</p>', unsafe_allow_html=True)
authenticator.login(location='sidebar')

auth_status = st.session_state.get('authentication_status')

# --- 4. LOGICA VISUALIZZAZIONE ---
if auth_status:
    name = st.session_state.get('name')
    st.sidebar.success(f"Online: {name}")
    authenticator.logout('Logout', 'sidebar')
    
    st.title("🏮 DATABASE ATTIVO")
    
    categoria = st.selectbox("SCEGLI CATEGORIA:", ["IN CORSO", "PROSSIMAMENTE", "TOP RATED"])
    url_map = {"IN CORSO": "seasons/now", "PROSSIMAMENTE": "seasons/upcoming", "TOP RATED": "top/anime"}

    try:
        res = requests.get(f"https://jikan.moe{url_map[categoria]}").json().get('data', [])[:12]
        cols = st.columns(3)
        for i, anime in enumerate(res):
            with cols[i % 3]:
                st.markdown(f"""
                    <div class="anime-card">
                        <img src="{anime['images']['jpg']['large_image_url']}" style="width:100%; height:300px; object-fit:cover; border-radius:10px;">
                        <h4 style="color:#00d4ff; margin-top:10px;">{anime['title'][:30]}</h4>
                    </div>
                """, unsafe_allow_html=True)
                st.link_button("DETTAGLI", anime['url'])
    except:
        st.error("Errore nel caricamento dei dati dal database.")

else:
    # SCHERMATA DI BENVENUTO
    st.title("🏯 ACCESSO PROTETTO")
    # Immagine di benvenuto da GitHub
    st.image(URL_BENVENUTO, use_container_width=True)
    
    with st.sidebar.expander("🆕 REGISTRATI"):
        try:
            if authenticator.register_user(location='sidebar'):
                st.success('Registrato! Accedi sopra.')
        except Exception as e:
            st.error(f"Errore: {e}")
    
    st.warning("Identificati nella barra laterale per sbloccare i file riservati.")
