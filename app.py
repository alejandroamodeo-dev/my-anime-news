
import streamlit as st
import requests
import streamlit_authenticator as stauth
import json
import os
from datetime import datetime

# --- 1. CONFIGURAZIONE E STILE MANGA (TOTAL BLACK + NEON) ---
st.set_page_config(page_title="My Anime News Pro", page_icon="🏮", layout="wide")

# Script per traduzione automatica (Google Translate)
st.markdown("""
    <div id="google_translate_element" style="position: fixed; top: 10px; right: 10px; z-index: 1001;"></div>
    <script type="text/javascript">
        function googleTranslateElementInit() {
            new google.translate.TranslateElement({pageLanguage: 'it', layout: google.translate.TranslateElement.InlineLayout.SIMPLE}, 'google_translate_element');
        }
    </script>
    <script type="text/javascript" src="//://google.com"></script>
    
    <style>
    /* SFONDO MANGA INTERO */
    .stApp {
        background-image: url("https://imgur.com");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }

    /* Rende trasparenti i contenitori di Streamlit */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMainViewContainer"] {
        background-color: rgba(0, 0, 0, 0) !important;
    }

    /* Velo scuro per la leggibilità del contenuto centrale */
    .main .block-container {
        background-color: rgba(0, 0, 0, 0.7);
        border-radius: 20px;
        padding: 40px;
        margin-top: 20px;
        border: 1px solid rgba(255, 75, 75, 0.3);
    }
    
    /* SIDEBAR SCURA */
    [data-testid="stSidebar"] { 
        background-color: rgba(5, 5, 5, 0.95) !important; 
        border-right: 2px solid #ff4b4b; 
    }
    
    /* LOGO GIGANTE ANIMATO */
    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
    .logo-text {
        font-size: 48px !important;
        font-weight: 900;
        color: #ff4b4b !important;
        text-align: center;
        text-shadow: 2px 2px 15px rgba(255, 75, 75, 0.8);
        animation: pulse 2s infinite;
        line-height: 1;
    }

    /* CARD ANIME NEON */
    .anime-card {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 20px;
        color: #000 !important;
        border: 2px solid #ff4b4b;
        transition: 0.3s;
    }
    .anime-card:hover { transform: translateY(-10px); border-color: #00ff41; }
    
    /* CHAT BOX */
    .chat-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        height: 350px;
        overflow-y: auto;
        border: 1px solid #ff4b4b;
    }

    h1, h2, h3 { color: #ff4b4b !important; text-shadow: 2px 2px 5px #000; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTIONE CHAT ---
def load_chat():
    if not os.path.exists("chat_pro.json"): return []
    with open("chat_pro.json", "r") as f: return json.load(f)

def save_chat(msgs):
    with open("chat_pro.json", "w") as f: json.dump(msgs, f)

# --- 3. SISTEMA ACCOUNT ---
if 'users' not in st.session_state:
    st.session_state['users'] = {"usernames": {"admin": {"name": "Admin", "password": "123", "email": "admin@anime.it"}}}

authenticator = stauth.Authenticate(st.session_state['users'], "anime_pro_key", "sig_key", cookie_expiry_days=30)
st.sidebar.markdown('<p class="logo-text">🏮<br>MY ANIME NEWS</p>', unsafe_allow_html=True)
authenticator.login(location='sidebar')

auth_status = st.session_state.get('authentication_status')

# --- 4. LOGICA SITO ---
if auth_status:
    name = st.session_state.get('name')
    st.sidebar.success(f"Online: {name}")
    authenticator.logout('Logout', 'sidebar')
    
    menu = st.tabs(["📺 NEWS & DATABASE", "💬 CHAT COMMUNITY"])

    with menu[0]:
        st.title("🏮 DATABASE ATTIVO")
        cat = st.selectbox("CATEGORIA:", ["IN CORSO", "PROSSIMAMENTE", "TOP RATED"])
        url_map = {"IN CORSO": "seasons/now", "PROSSIMAMENTE": "seasons/upcoming", "TOP RATED": "top/anime"}
        
        try:
            res = requests.get(f"https://jikan.moe{url_map[cat]}").json().get('data', [])[:9]
            cols = st.columns(3)
            for i, anime in enumerate(res):
                with cols[i % 3]:
                    st.markdown(f"""
                        <div class="anime-card">
                            <img src="{anime['images']['jpg']['large_image_url']}" style="width:100%; height:300px; object-fit:cover; border-radius:10px;">
                            <h4 style="color:black; margin-top:10px;">{anime['title'][:25]}</h4>
                            <p style="color:#444;">⭐ Voto: {anime.get('score', 'N/A')}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    # Commenti e voti individuali
                    voto = st.slider(f"Valuta {i}", 1, 10, 5, key=f"v_{i}")
                    if st.button(f"Invia Voto", key=f"b_{i}"): st.toast("Voto registrato!")
                    st.link_button("DETTAGLI", anime['url'])
        except: st.error("Errore API.")

    with menu[1]:
        st.title("💬 CHAT GLOBALE")
        msgs = load_chat()
        chat_html = "".join([f"<p style='margin-bottom:5px;'><b>{m['u']}</b>: {m['t']}</p>" for m in msgs[-20:]])
        st.markdown(f'<div class="chat-container">{chat_html}</div>', unsafe_allow_html=True)
        
