import streamlit as st
import requests
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px
import json

# --- 1. CONFIGURAZIONE & STILE ---
st.set_page_config(page_title="My Anime News Pro", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    .stApp { background: #1a1a1d; color: #f0f0f0; font-family: 'Rajdhani', sans-serif; }
    
    /* Sakura Giganti */
    .sakura-container { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; }
    .petal { position: absolute; background-color: #ffb7c5; border-radius: 150% 0 150% 0; opacity: 0.5; animation: fall linear infinite; }
    @keyframes fall { 0% { transform: translateY(-100px) rotate(0deg); opacity: 0; } 100% { transform: translateY(100vh) rotate(360deg); opacity: 0; } }

    /* Neon Logo */
    .anime-logo {
        font-family: 'Bangers', cursive; font-size: 7rem; text-align: center; color: #fff;
        text-shadow: 0 0 10px #ff4b4b, 0 0 30px #ff4b4b; margin-top: -40px;
    }
    
    .fresh-card {
        background: rgba(255, 255, 255, 0.05); border: 2px solid rgba(255, 75, 75, 0.3);
        border-radius: 20px; padding: 20px; backdrop-filter: blur(10px); transition: 0.3s;
    }
    .fresh-card:hover { border-color: #ff4b4b; box-shadow: 0 0 30px rgba(255, 75, 75, 0.4); transform: translateY(-5px); }
    </style>
    
    <div class="sakura-container">
        <div class="petal" style="width:30px; height:30px; left:10%; animation-duration:10s;"></div>
        <div class="petal" style="width:40px; height:40px; left:40%; animation-duration:15s;"></div>
        <div class="petal" style="width:35px; height:35px; left:80%; animation-duration:12s;"></div>
    </div>
""", unsafe_allow_html=True)

# --- 2. SISTEMA ACCOUNT ---
if 'config' not in st.session_state:
    st.session_state.config = {
        "credentials": {"usernames": {"admin": {"name": "Boss", "password": "$2b$12$K7T6U/f0XpM9kPzN8Ff1.O6R5T7n5.N0v4P0E7S6Z.k6W/F7f5W2K", "email": "a@b.com"}}},
        "cookie": {"key": "sakura_v6", "name": "man_cookie", "expiry_days": 30}
    }

authenticator = stauth.Authenticate(st.session_state.config['credentials'], "man_cookie", "sakura_v6", 30)
authenticator.login(location='sidebar')

auth_status = st.session_state.get("authentication_status")
name = st.session_state.get("name")

# --- 3. LOGICA APP ---
if auth_status:
    st.sidebar.markdown(f"### 🏮 Shinobi: **{name}**")
    menu = st.sidebar.selectbox("VAI A:", ["🏠 News Fresche", "💬 AI Chat Personaggi", "📊 Sondaggi Community", "📂 Mia Watchlist", "🖼️ Fan Art"])
    authenticator.logout('Logout', 'sidebar')

    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)

    if menu == "🏠 News Fresche":
        st.markdown("<h2 style='text-align:center; color:#ffb7c5;'>ULTIME USCITE GIAPPONESI</h2>", unsafe_allow_html=True)
        res = requests.get("https://jikan.moe").json().get('data', [])[:6]
        cols = st.columns(3)
        for i, anime in enumerate(res):
            with cols[i % 3]:
                st.markdown(f"""<div class="fresh-card">
                    <img src="{anime['images']['jpg']['large_image_url']}" style="width:100%; height:250px; object-fit:cover; border-radius:15px;">
                    <h3 style="color:#ff4b4b; margin-top:10px;">{anime['title'][:25]}</h3>
                    <p>⭐ Score: {anime.get('score', 'N/A')}</p>
                </div>""", unsafe_allow_html=True)
                if st.button(f"Salva in Watchlist", key=f"w_{i}"):
                    if 'wl' not in st.session_state: st.session_state.wl = []
                    st.session_state.wl.append(anime['title'])
                    st.toast("Salvato!")

    elif menu == "💬 AI Chat Personaggi":
        st.subheader("Simulatore di Conversazione Anime")
        char = st.radio("Con chi vuoi parlare?", ["Naruto", "Luffy", "Saitama"], horizontal=True)
        if "chat_history" not in st.session_state: st.session_state.chat_history = []
        
        user_input = st.chat_input("Chiedi qualcosa...")
        if user_input:
            st.session_state.chat_history.append(("user", user_input))
            resp = {"Naruto": "Dattebayo! Non mi arrenderò mai!", "Luffy": "Carneee! Sei dei miei?", "Saitama": "Ok."}
            st.session_state.chat_history.append(("assistant", resp[char]))
        
        for role, text in st.session_state.chat_history[-6:]:
            st.chat_message(role).write(text)

    elif menu == "📊 Sondaggi Community":
        st.subheader("Qual è lo studio di animazione migliore?")
        voti = st.session_state.get('voti', {"MAPPA": 20, "Ufotable": 35, "Wit Studio": 15})
        scelta = st.radio("Vota:", list(voti.keys()))
        if st.button("Vota ora"):
            voti[scelta] += 1
            st.session_state.voti = voti
            st.rerun()
        fig = px.pie(names=list(voti.keys()), values=list(voti.values()), hole=0.4, template="plotly_dark", color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)

    elif menu == "📂 Mia Watchlist":
        st.subheader("Anime da non perdere")
        lista = st.session_state.get('wl', [])
        if lista:
            for a in set(lista): st.write(f"✅ {a}")
        else: st.info("Lista vuota!")

    elif menu == "🖼️ Fan Art":
        st.subheader("Carica le tue opere")
        img = st.file_uploader("Scegli un'immagine", type=['png', 'jpg'])
        if img: st.image(img, caption="La tua Fan Art", use_container_width=True)

else:
    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>ACCEDI DAL MENU LATERALE</h2>", unsafe_allow_html=True)
    with st.sidebar.expander("Non hai un account? Registrati"):
        if authenticator.register_user(location='main', pre_authorization=[]):
            st.success('Registrato! Accedi ora.')
