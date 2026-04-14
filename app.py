import streamlit as st
import requests
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import os

# --- 1. CONFIGURAZIONE & DESIGN SAUVAGE ---
st.set_page_config(page_title="My Anime News - Fresh Edition", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    .stApp { background: #050508; color: #f0f0f0; font-family: 'Rajdhani', sans-serif; }
    
    /* Petali Sakura Giganti */
    .sakura-container { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 9999; }
    .petal { position: absolute; background-color: #ffb7c5; border-radius: 150% 0 150% 0; opacity: 0.8; filter: drop-shadow(0 0 8px #ffb7c5); animation: fall linear infinite; }
    @keyframes fall { 0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; } 100% { transform: translateY(110vh) rotate(720deg); opacity: 0; } }

    /* Logo Gigante e Testo Bianco */
    .anime-logo { font-family: 'Bangers', cursive; font-size: clamp(6rem, 15vw, 12rem); text-align: center; color: #fff; text-shadow: 0 0 20px #ff4b4b, 0 0 40px #ff4b4b, 0 0 80px #ff4b4b; margin-top: -120px; line-height: 0.9; }
    .fresche-title { text-align: center; font-size: clamp(1rem, 3vw, 1.8rem); color: #ffffff !important; font-weight: 700; letter-spacing: 12px; margin-top: -10px; margin-bottom: 60px; text-transform: uppercase; }

    .fresh-card { background: rgba(45, 45, 50, 0.9); border: 2px solid rgba(255, 75, 75, 0.4); border-radius: 15px; padding: 25px; backdrop-filter: blur(10px); height: 520px; transition: 0.3s; }
    .fresh-card:hover { border-color: #ff4b4b; box-shadow: 0 0 30px rgba(255, 75, 75, 0.6); transform: scale(1.02); }
    </style>
    <div class="sakura-container">
        <div class="petal" style="width:35px; height:35px; left:5%; animation-duration:8s;"></div>
        <div class="petal" style="width:50px; height:50px; left:25%; animation-duration:12s;"></div>
        <div class="petal" style="width:65px; height:65px; left:80%; animation-duration:15s;"></div>
    </div>
""", unsafe_allow_html=True)

# --- 2. SISTEMA ACCOUNT ---
if 'config' not in st.session_state:
    st.session_state.config = {"credentials": {"usernames": {"admin": {"name": "Capo", "password": "$2b$12$K7T6U/f0XpM9kPzN8Ff1.O6R5T7n5.N0v4P0E7S6Z.k6W/F7f5W2K", "email": "a@b.com"}}}, "cookie": {"key": "sakura_v12", "name": "man_cookie", "expiry_days": 30}}

authenticator = stauth.Authenticate(st.session_state.config['credentials'], "man_cookie", "sakura_v12", 30)
authenticator.login(location='sidebar')
auth_status = st.session_state.get("authentication_status")
name = st.session_state.get("name")

# --- 3. LOGICA NEWS AUTOMATICHE (CACHED) ---
@st.cache_data(ttl=600) # Evita il rate limit del server
def get_fresh_news():
    try:
        # Endpoint per le serie attualmente in corso (fresche)
        r = requests.get("https://jikan.moe", timeout=10)
        if r.status_code == 200:
            return r.json().get('data', [])[:9]
        return []
    except: return []

# --- 4. APP LOGIC ---
if auth_status:
    st.sidebar.write(f"🏮 Shinobi: **{name}**")
    menu = st.sidebar.radio("SISTEMA", ["🏠 News Fresche", "💬 AI Chat Personaggi", "📊 Mega Sondaggio", "📂 Mia Watchlist"])
    authenticator.logout('Logout', 'sidebar')

    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    st.markdown('<p class="fresche-title">INFORMAZIONI ANIME FRESCHE</p>', unsafe_allow_html=True)

    if menu == "🏠 News Fresche":
        news_data = get_fresh_news()
        if news_data:
            cols = st.columns(3)
            for i, anime in enumerate(news_data):
                with cols[i % 3]:
                    img = anime.get('images', {}).get('jpg', {}).get('large_image_url', '')
                    st.markdown(f"""<div class="fresh-card">
                        <img src="{img}" style="width:100%; height:280px; object-fit:cover; border-radius:10px;">
                        <h4 style="color:#ff4b4b; margin-top:10px;">{anime.get('title', 'N/D')[:35]}</h4>
                        <p style="color:#ccc; font-size:0.9rem;">Studio: {anime.get('studios', [{'name':'N/D'}])[0].get('name', 'N/D')}</p>
                    </div>""", unsafe_allow_html=True)
                    if st.button(f"Salva in Watchlist", key=f"w_{i}"):
                        if 'wl' not in st.session_state: st.session_state.wl = []
                        st.session_state.wl.append(anime['title']); st.toast("✅ Salvato!")
        else:
            st.warning("🏮 Server Jikan momentaneamente occupato. Riprova tra 5 secondi.")

    elif menu == "💬 AI Chat Personaggi":
        char = st.selectbox("Chi vuoi evocare?", ["Naruto Uzumaki", "Monkey D. Luffy", "Satoru Gojo", "Saitama"])
        resps = {"Naruto Uzumaki": "Dattebayo! Non mi arrenderò mai!", "Monkey D. Luffy": "Io diventerò il Re dei Pirati!", "Satoru Gojo": "Io sono il più forte.", "Saitama": "Ok."}
        msg = st.chat_input(f"Parla con {char}...")
        if msg:
            st.chat_message("user").write(msg)
            st.chat_message("assistant").write(resps[char])

    elif menu == "📊 Mega Sondaggio":
        if 'votes' not in st.session_state: st.session_state.votes = {"One Piece": 50, "Solo Leveling": 45, "Bleach": 30, "Naruto": 40}
        pick = st.radio("Vota l'Anime Definitivo:", list(st.session_state.votes.keys()))
        if st.button("Vota"):
            st.session_state.votes[pick] += 1
            st.success("Voto registrato!"); st.rerun()
        df = pd.DataFrame(list(st.session_state.votes.items()), columns=['Anime', 'Voti'])
        st.plotly_chart(px.bar(df, x='Anime', y='Voti', color='Anime', template="plotly_dark"))

    elif menu == "📂 Mia Watchlist":
        for a in set(st.session_state.get('wl', [])): st.write(f"📺 {a}")

elif auth_status is None:
    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    with st.sidebar.expander("Non hai un account? Registrati"):
        if authenticator.register_user(location='main', preauthorization=False):
            st.success('Registrato! Accedi ora.')
