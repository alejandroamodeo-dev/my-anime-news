import streamlit as st
import requests
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. CONFIGURAZIONE & DESIGN "ULTRA NEON" ---
st.set_page_config(page_title="My Anime News - Ultimate", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    @import url('https://googleapis.com');

    .stApp {
        background: #1a1a1d;
        background-image: radial-gradient(circle at 50% 50%, #25252b 0%, #1a1a1d 100%);
        color: #f0f0f0;
        font-family: 'Rajdhani', sans-serif;
    }

    /* PETALI SAKURA GIGANTI */
    .sakura-container { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; }
    .petal { position: absolute; background-color: #ffb7c5; border-radius: 150% 0 150% 0; opacity: 0.6; animation: fall linear infinite; }
    @keyframes fall { 0% { transform: translateY(-100px) rotate(0deg); opacity: 0; } 100% { transform: translateY(100vh) rotate(360deg); opacity: 0; } }

    /* LOGO GIGANTE 10REM CON NEON FIGO */
    .anime-logo {
        font-family: 'Bangers', cursive;
        font-size: 10rem; /* GRANDEZZA MASSIMA */
        text-align: center;
        color: #fff;
        text-shadow: 0 0 15px #ff4b4b, 0 0 30px #ff4b4b, 0 0 60px #ff4b4b;
        animation: neonPulse 1.5s ease-in-out infinite alternate;
        margin-top: -60px;
        margin-bottom: 10px;
    }

    @keyframes neonPulse {
        from { text-shadow: 0 0 10px #ff4b4b, 0 0 20px #ff4b4b, 0 0 40px #ff4b4b; }
        to { text-shadow: 0 0 5px #ff4b4b, 0 0 15px #ff4b4b, 0 0 25px #ff4b4b; }
    }

    .fresche-title {
        text-align: center;
        font-size: 2.2rem;
        color: #ffb7c5;
        font-weight: 700;
        letter-spacing: 8px;
        margin-bottom: 40px;
        text-transform: uppercase;
    }

    .fresh-card {
        background: rgba(45, 45, 50, 0.9);
        border: 2px solid rgba(255, 75, 75, 0.3);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
        transition: 0.3s;
    }
    .fresh-card:hover { border-color: #ff4b4b; box-shadow: 0 0 25px rgba(255, 75, 75, 0.5); }
    </style>

    <div class="sakura-container">
        <div class="petal" style="width:30px; height:30px; left:10%; animation-duration:10s;"></div>
        <div class="petal" style="width:40px; height:40px; left:35%; animation-duration:15s;"></div>
        <div class="petal" style="width:35px; height:35px; left:75%; animation-duration:12s;"></div>
    </div>
""", unsafe_allow_html=True)

# --- 2. SISTEMA ACCOUNT ---
if 'config' not in st.session_state:
    st.session_state.config = {
        "credentials": {
            "usernames": {
                "admin": {"name": "Boss", "password": "$2b$12$K7T6U/f0XpM9kPzN8Ff1.O6R5T7n5.N0v4P0E7S6Z.k6W/F7f5W2K", "email": "a@b.com"}
            }
        },
        "cookie": {"key": "sakura_v7", "name": "man_cookie", "expiry_days": 30}
    }

authenticator = stauth.Authenticate(
    st.session_state.config['credentials'],
    st.session_state.config['cookie']['name'],
    st.session_state.config['cookie']['key'],
    st.session_state.config['cookie']['expiry_days']
)

# Login
authenticator.login(location='sidebar')
auth_status = st.session_state.get("authentication_status")
name = st.session_state.get("name")

# --- 3. CONTENUTO APP ---
if auth_status:
    st.sidebar.write(f"🏮 Shinobi: **{name}**")
    menu = st.sidebar.radio("NAVIGAZIONE", ["🏠 News", "💬 AI Chat", "📊 Sondaggi", "📂 Watchlist"])
    authenticator.logout('Logout', 'sidebar')

    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    st.markdown('<p class="fresche-title">INFORMAZIONI ANIME FRESCHE</p>', unsafe_allow_html=True)

    if menu == "🏠 News":
        try:
            res = requests.get("https://jikan.moe").json().get('data', [])[:6]
            cols = st.columns(3)
            for i, anime in enumerate(res):
                with cols[i % 3]:
                    st.markdown(f"""<div class="fresh-card">
                        <img src="{anime['images']['jpg']['large_image_url']}" style="width:100%; height:200px; object-fit:cover; border-radius:10px;">
                        <h4 style="color:#ff4b4b; margin-top:10px;">{anime['title'][:30]}</h4>
                    </div>""", unsafe_allow_html=True)
                    if st.button(f"Salva", key=f"w_{i}"):
                        if 'wl' not in st.session_state: st.session_state.wl = []
                        st.session_state.wl.append(anime['title'])
                        st.toast("Salvato!")
        except: st.error("Errore News API.")

    elif menu == "💬 AI Chat":
        st.subheader("Chatta con i Personaggi")
        char = st.selectbox("Scegli:", ["Naruto", "Luffy"])
        msg = st.chat_input("Scrivi...")
        if msg:
            st.chat_message("user").write(msg)
            st.chat_message("assistant").write("Dattebayo! Sto mangiando ramen ora!" if char=="Naruto" else "Voglio carne!")

    elif menu == "📊 Sondaggi":
        st.subheader("Vota l'Anime della Stagione")
        votes = st.session_state.get('votes', {"Bleach": 10, "One Piece": 15})
        pick = st.radio("Vota:", list(votes.keys()))
        if st.button("Invia"):
            votes[pick] += 1
            st.session_state.votes = votes
            st.rerun()
        st.plotly_chart(px.bar(x=list(votes.keys()), y=list(votes.values()), template="plotly_dark"))

    elif menu == "📂 Watchlist":
        st.subheader("La tua lista")
        for a in set(st.session_state.get('wl', [])): st.write(f"📺 {a}")

elif auth_status is False:
    st.sidebar.error("Credenziali errate.")

# --- REGISTRAZIONE (FIXED PARAMETERS) ---
if auth_status is None:
    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    with st.sidebar.expander("Non hai un account? Registrati"):
        try:
            # Per le versioni recenti, non passare pre_authorization se dà errore
            # oppure usa la sintassi base location='main'
            if authenticator.register_user(location='main'):
                st.success('Registrato! Effettua il login.')
        except Exception as e:
            st.error(f"Errore registrazione: {e}")
    st.markdown("<div style='text-align:center;'><h2>ACCEDI DALLA SIDEBAR</h2></div>", unsafe_allow_html=True)
