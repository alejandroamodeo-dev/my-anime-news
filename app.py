import streamlit as st
import requests
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. CONFIGURAZIONE & DESIGN "SAKURA NEON ELITE" ---
st.set_page_config(page_title="My Anime News - Ultimate", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    @import url('https://googleapis.com');

    .stApp {
        background: #050508 !important;
        background-image: radial-gradient(circle at 50% 50%, #1a1a2e 0%, #050508 100%) !important;
        color: #f0f0f0;
        font-family: 'Rajdhani', sans-serif;
    }

    /* PETALI SAKURA GIGANTI - VISIBILI SOPRA TUTTO */
    .sakura-container {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        pointer-events: none;
        z-index: 9999;
    }
    .petal {
        position: absolute;
        background-color: #ffb7c5;
        border-radius: 150% 0 150% 0;
        opacity: 0.8;
        filter: drop-shadow(0 0 8px #ffb7c5);
        animation: fall linear infinite;
    }
    @keyframes fall {
        0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; }
        10% { opacity: 0.8; }
        100% { transform: translateY(110vh) rotate(720deg); opacity: 0; }
    }

    /* LOGO GIGANTE QUASI IN CIMA */
    .anime-logo {
        font-family: 'Bangers', cursive;
        font-size: clamp(6rem, 15vw, 12rem); 
        text-align: center;
        color: #fff;
        text-shadow: 0 0 20px #ff4b4b, 0 0 40px #ff4b4b, 0 0 80px #ff4b4b;
        animation: neonPulse 1.8s ease-in-out infinite alternate;
        margin-top: -120px; /* Quasi in cima */
        line-height: 0.9;
        white-space: nowrap;
    }

    /* SCRITTA SOTTO BIANCA PIÙ PICCOLA */
    .fresche-title {
        text-align: center;
        font-size: clamp(1rem, 3vw, 1.8rem);
        color: #ffffff !important; /* Bianca */
        font-weight: 700;
        letter-spacing: 12px;
        margin-top: -10px;
        margin-bottom: 60px;
        text-transform: uppercase;
        opacity: 0.9;
    }

    @keyframes neonPulse {
        from { text-shadow: 0 0 20px #ff4b4b, 0 0 40px #ff4b4b, 0 0 80px #ff4b4b; }
        to { text-shadow: 0 0 10px #ff4b4b, 0 0 20px #ff4b4b, 0 0 40px #ff4b4b; }
    }

    .fresh-card {
        background: rgba(45, 45, 50, 0.9);
        border: 2px solid rgba(255, 75, 75, 0.4);
        border-radius: 15px;
        padding: 25px;
        backdrop-filter: blur(10px);
    }
    </style>

    <div class="sakura-container">
        <div class="petal" style="width:35px; height:35px; left:5%; animation-duration:8s;"></div>
        <div class="petal" style="width:50px; height:50px; left:25%; animation-duration:12s;"></div>
        <div class="petal" style="width:40px; height:40px; left:55%; animation-duration:10s;"></div>
        <div class="petal" style="width:65px; height:65px; left:80%; animation-duration:15s;"></div>
    </div>
""", unsafe_allow_html=True)

# --- 2. SISTEMA ACCOUNT ---
if 'config' not in st.session_state:
    st.session_state.config = {
        "credentials": {
            "usernames": {
                "admin": {"name": "Redattore Capo", "password": "$2b$12$K7T6U/f0XpM9kPzN8Ff1.O6R5T7n5.N0v4P0E7S6Z.k6W/F7f5W2K", "email": "admin@myanimenews.it"}
            }
        },
        "cookie": {"key": "sakura_v9", "name": "man_cookie", "expiry_days": 30}
    }

authenticator = stauth.Authenticate(
    st.session_state.config['credentials'],
    st.session_state.config['cookie']['name'],
    st.session_state.config['cookie']['key'],
    st.session_state.config['cookie']['expiry_days']
)

# LOGIN
authenticator.login(location='sidebar')
auth_status = st.session_state.get("authentication_status")
name = st.session_state.get("name")

# --- 3. CONTENUTO ---
if auth_status:
    st.sidebar.write(f"🏮 Shinobi: **{name}**")
    menu = st.sidebar.radio("SISTEMA", ["🏠 News", "💬 AI Chat", "📊 Sondaggi", "📂 Watchlist"])
    authenticator.logout('Logout', 'sidebar')

    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    st.markdown('<p class="fresche-title">INFORMAZIONI ANIME FRESCHE</p>', unsafe_allow_html=True)

    if menu == "🏠 News":
        try:
            res = requests.get("https://jikan.moe", timeout=10).json().get('data', [])[:6]
            cols = st.columns(3)
            for i, anime in enumerate(res):
                with cols[i % 3]:
                    st.markdown(f"""<div class="fresh-card">
                        <img src="{anime['images']['jpg']['large_image_url']}" style="width:100%; height:250px; object-fit:cover; border-radius:10px;">
                        <h4 style="color:#ff4b4b; margin-top:10px;">{anime['title'][:35]}</h4>
                    </div>""", unsafe_allow_html=True)
                    if st.button(f"Salva", key=f"w_{i}"):
                        if 'wl' not in st.session_state: st.session_state.wl = []
                        st.session_state.wl.append(anime['title'])
                        st.toast(f"✅ {anime['title']} salvato!")
        except: st.error("Errore API.")

elif auth_status is False:
    st.sidebar.error("Credenziali errate.")

# REGISTRAZIONE (FIXED PER ULTIMA VERSIONE)
if auth_status is None:
    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    with st.sidebar.expander("Non hai un account? Registrati"):
        try:
            # preauthorization=False abilita la registrazione a tutti
            if authenticator.register_user(location='main', preauthorization=False):
                st.success('Registrato! Accedi ora.')
        except Exception as e:
            st.error(f"Errore: {e}")
