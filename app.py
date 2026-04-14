import streamlit as st
import requests
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px
from datetime import datetime
import time

# --- 1. DESIGN "SAKURA NEON ELITE" ---
st.set_page_config(page_title="My Anime News - Ultimate", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    .stApp { background: #050508; color: #f0f0f0; font-family: 'Rajdhani', sans-serif; }

    /* FIX FOGLIE: GIGANTI, ROSA ACCESO E SOPRA TUTTO */
    .sakura-container {
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        pointer-events: none;
        z-index: 99999;
    }

    .petal {
        position: absolute;
        background-color: #ffb7c5;
        border-radius: 150% 0 150% 0;
        opacity: 0.8;
        filter: drop-shadow(0 0 12px #ffb7c5);
        animation: fall linear infinite;
    }

    @keyframes fall {
        0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; }
        10% { opacity: 0.8; }
        100% { transform: translateY(110vh) rotate(720deg); opacity: 0; }
    }

    /* TITOLO GIGANTE 12REM QUASI IN CIMA */
    .anime-logo { 
        font-family: 'Bangers', cursive; 
        font-size: clamp(6rem, 18vw, 12rem); 
        text-align: center; 
        color: #fff; 
        text-shadow: 0 0 20px #ff4b4b, 0 0 40px #ff4b4b, 0 0 80px #ff4b4b; 
        margin-top: -120px; 
        line-height: 0.9; 
    }

    /* SCRITTA SOTTO BIANCA */
    .fresche-title { 
        text-align: center; 
        font-size: clamp(1rem, 3vw, 1.8rem); 
        color: #ffffff !important; 
        font-weight: 700; 
        letter-spacing: 12px; 
        margin-top: -10px; 
        margin-bottom: 60px; 
        text-transform: uppercase; 
    }

    .fresh-card { 
        background: rgba(45, 45, 50, 0.9); 
        border: 2px solid rgba(255, 75, 75, 0.4); 
        border-radius: 15px; 
        padding: 25px; 
        backdrop-filter: blur(10px); 
        height: 520px; 
    }
    </style>

    <div class="sakura-container">
        <div class="petal" style="width:50px; height:50px; left:5%; animation-duration:7s;"></div>
        <div class="petal" style="width:65px; height:65px; left:25%; animation-duration:12s;"></div>
        <div class="petal" style="width:40px; height:40px; left:45%; animation-duration:10s;"></div>
        <div class="petal" style="width:80px; height:80px; left:70%; animation-duration:15s;"></div>
        <div class="petal" style="width:55px; height:55px; left:90%; animation-duration:11s;"></div>
    </div>
""", unsafe_allow_html=True)

# --- 2. SISTEMA ACCOUNT (FIX CHIAVI RESET) ---
if 'config' not in st.session_state:
    st.session_state.config = {
        "credentials": {
            "usernames": {
                "admin": {
                    "name": "Redattore Capo", 
                    "password": "$2b$12$K7T6U/f0XpM9kPzN8Ff1.O6R5T7n5.N0v4P0E7S6Z.k6W/F7f5W2K", 
                    "email": "admin@myanimenews.it"
                }
            }
        },
        "cookie": {
            "key": "anime_nexus_mega_key_2024", # Chiave resettata
            "name": "man_cookie_vFinal",        # Nome cookie cambiato
            "expiry_days": 30
        }
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

# --- 3. LOGICA NEWS CON CACHE ---
@st.cache_data(ttl=600)
def get_fresh_news():
    try:
        r = requests.get("https://jikan.moe", timeout=10)
        if r.status_code == 200: return r.json().get('data', [])[:9]
    except: pass
    return []

# --- 4. CHAT INTELLIGENTE ---
def get_ai_response(char, user_text):
    t = user_text.lower()
    res = {
        "Naruto": {"ramen": "Ichiraku! Offro io, dattebayo!", "sogno": "Hokage! È il mio destino!", "default": "Non mollare mai!"},
        "Luffy": {"carne": "CARNEEE! Ne voglio mille chili!", "re": "Sarò il Re dei Pirati!", "default": "Shishishi! Sei forte!"},
        "Gojo": {"forte": "Io sono l'Infinito. Nessuno mi tocca.", "dolci": "Hai dei Mochi? Li adoro!", "default": "Tranquillo, ci sono io."}
    }
    char_res = res.get(char, res["Naruto"])
    for k in char_res:
        if k in t: return char_res[k]
    return char_res["default"]

# --- 5. LOGICA APP ---
if auth_status:
    st.sidebar.write(f"🏮 Shinobi: **{name}**")
    menu = st.sidebar.radio("SISTEMA", ["🏠 News", "💬 Chat Eroi", "📂 Watchlist"])
    authenticator.logout('Logout', 'sidebar')

    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    st.markdown('<p class="fresche-title">INFORMAZIONI ANIME FRESCHE</p>', unsafe_allow_html=True)

    if menu == "🏠 News":
        news = get_fresh_news()
        if news:
            cols = st.columns(3)
            for i, a in enumerate(news):
                with cols[i % 3]:
                    st.markdown(f"""<div class="fresh-card">
                        <img src="{a['images']['jpg']['large_image_url']}" style="width:100%; height:280px; object-fit:cover; border-radius:10px;">
                        <h4 style="color:#ff4b4b; margin-top:10px;">{a.get('title')[:30]}</h4>
                        <p style="color:#ccc;">⭐ Score: {a.get('score', 'N/A')}</p>
                    </div>""", unsafe_allow_html=True)
        else:
            st.warning("🏮 Server occupati. Riprova tra poco.")

    elif menu == "💬 Chat Eroi":
        char = st.selectbox("Evoca:", ["Naruto", "Luffy", "Gojo"])
        msg = st.chat_input("Parla con l'eroe...")
        if msg:
            st.chat_message("user").write(msg)
            st.chat_message("assistant").write(get_ai_response(char, msg))

elif auth_status is None:
    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    with st.sidebar.expander("Non hai un account? Registrati"):
        try:
            # preauthorization=False per eliminare l'errore InvalidToken in fase di input
            if authenticator.register_user(location='main', preauthorization=False):
                st.success('Registrato! Ora fai il login.')
        except Exception as e:
            st.error(f"Errore: {e}")
