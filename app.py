import streamlit as st
import requests
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px
from datetime import datetime
import random

# --- 1. CONFIGURAZIONE & STYLE ---
st.set_page_config(page_title="My Anime News - Ultimate Portal", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    .stApp { background: #1a1a1d; color: #f0f0f0; font-family: 'Rajdhani', sans-serif; }
    
    /* Sakura Petals */
    .sakura-container { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; }
    .petal { position: absolute; background-color: #ffb7c5; border-radius: 150% 0 150% 0; opacity: 0.6; animation: fall linear infinite; }
    @keyframes fall { 0% { transform: translateY(-100px) rotate(0deg); opacity: 0; } 10% { opacity: 0.8; } 100% { transform: translateY(100vh) rotate(360deg); opacity: 0; } }
    
    .anime-logo { font-family: 'Bangers', cursive; font-size: 5rem; text-align: center; color: #ff4b4b; text-shadow: 0 0 20px #ff4b4b; margin-top: -20px; }
    .fresh-card { background: rgba(45, 45, 50, 0.9); border: 2px solid rgba(255, 75, 75, 0.3); border-radius: 15px; padding: 20px; backdrop-filter: blur(10px); transition: 0.3s; }
    .fresh-card:hover { border-color: #ff4b4b; box-shadow: 0 0 20px rgba(255, 75, 75, 0.5); }
    </style>
    <div class="sakura-container">
        <div class="petal" style="width:25px; height:25px; left:10%; animation-duration:10s;"></div>
        <div class="petal" style="width:30px; height:30px; left:30%; animation-duration:15s;"></div>
        <div class="petal" style="width:20px; height:20px; left:60%; animation-duration:12s;"></div>
    </div>
""", unsafe_allow_html=True)

# --- 2. STATO DELLA SESSIONE (Dati Persistenti) ---
if 'watchlist' not in st.session_state: st.session_state.watchlist = []
if 'poll_data' not in st.session_state: st.session_state.poll_data = {"One Piece": 10, "Naruto": 5, "Solo Leveling": 15}
if 'fan_arts' not in st.session_state: st.session_state.fan_arts = []

# --- 3. SISTEMA ACCOUNT ---
config = {
    "credentials": {"usernames": {"admin": {"name": "Boss", "password": "$2b$12$K7T6U/f0XpM9kPzN8Ff1.O6R5T7n5.N0v4P0E7S6Z.k6W/F7f5W2K", "email": "a@b.com"}}},
    "cookie": {"key": "sakura_ultimate", "name": "man_cookie", "expiry_days": 30}
}
authenticator = stauth.Authenticate(config['credentials'], config['cookie']['name'], config['cookie']['key'], config['cookie']['expiry_days'])

# --- 4. LOGICA APP ---
name, auth_status, username = authenticator.login(location='sidebar')

if auth_status:
    st.sidebar.title(f"Shinobi: {name}")
    menu = st.sidebar.radio("NAVIGAZIONE", ["🏠 Home & News", "💬 AI Character Chat", "🎮 Games & Quiz", "📊 Sondaggi Live", "📂 Watchlist", "🖼️ Fan Art Gallery"])
    authenticator.logout('Logout', 'sidebar')

    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)

    # --- HOME & NEWS ---
    if menu == "🏠 Home & News":
        st.subheader("🏮 Informazioni Anime Fresche")
        try:
            res = requests.get("https://jikan.moe").json().get('data', [])[:6]
            cols = st.columns(3)
            for i, anime in enumerate(res):
                with cols[i % 3]:
                    st.markdown(f"""<div class="fresh-card">
                        <img src="{anime['images']['jpg']['large_image_url']}" style="width:100%; height:200px; object-fit:cover; border-radius:10px;">
                        <h4 style="color:#ff4b4b;">{anime['title'][:30]}</h4>
                        <p>Studio: {anime.get('studios', [{'name':'N/D'}])[0]['name']}</p>
                    </div>""", unsafe_allow_html=True)
                    if st.button(f"Aggiungi a Watchlist", key=f"btn_{i}"):
                        if anime['title'] not in st.session_state.watchlist:
                            st.session_state.watchlist.append(anime['title'])
                            st.toast(f"✅ {anime['title']} aggiunto!")
        except: st.error("Errore News API.")

    # --- AI CHAT ---
    elif menu == "💬 AI Character Chat":
        st.subheader("Chatta con i tuoi Personaggi")
        char = st.selectbox("Scegli con chi parlare", ["Naruto", "Goku", "Luffy"])
        st.info(f"Stai parlando con **{char}**. (Simulazione AI attiva)")
        chat_input = st.chat_input("Scrivi qualcosa...")
        if chat_input:
            st.chat_message("user").write(chat_input)
            st.chat_message("assistant").write(f"Dattebayo! {name}, sono {char} e sono pronto a combattere!")

    # --- GAMES & QUIZ ---
    elif menu == "🎮 Games & Quiz":
        st.subheader("Testa la tua conoscenza!")
        q = st.radio("Chi è il protagonista di One Piece?", ["Luffy", "Zoro", "Sanji"])
        if st.button("Invia Risposta"):
            if q == "Luffy": st.success("CORRETTO! +10 punti Otaku")
            else: st.error("Sbagliato! Riprova.")

    # --- SONDAGGI LIVE ---
    elif menu == "📊 Sondaggi Live":
        st.subheader("Qual è l'anime dell'anno?")
        vote = st.selectbox("Vota ora:", list(st.session_state.poll_data.keys()))
        if st.button("Conferma Voto"):
            st.session_state.poll_data[vote] += 1
            st.rerun()
        df = pd.DataFrame(list(st.session_state.poll_data.items()), columns=['Anime', 'Voti'])
        fig = px.bar(df, x='Anime', y='Voti', color='Anime', template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    # --- WATCHLIST ---
    elif menu == "📂 Watchlist":
        st.subheader("La tua lista Anime")
        if st.session_state.watchlist:
            for item in st.session_state.watchlist:
                st.write(f"📺 {item}")
            if st.button("Svuota Lista"): st.session_state.watchlist = []; st.rerun()
        else: st.info("La tua lista è vuota. Aggiungi anime dalla Home!")

    # --- FAN ART ---
    elif menu == "🖼️ Fan Art Gallery":
        st.subheader("Condividi i tuoi disegni")
        uploaded_file = st.file_uploader("Carica una Fan Art", type=["jpg", "png"])
        if uploaded_file:
            st.image(uploaded_file, caption="La tua opera", use_container_width=True)
            st.success("Immagine caricata nella community!")

elif auth_status is False:
    st.sidebar.error("Credenziali errate.")

if not auth_status:
    with st.sidebar.expander("Non hai un account? Registrati"):
        if authenticator.register_user(location='main', pre_authorization=[]):
            st.success('Registrato! Accedi ora.')
    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;'><h2>ACCEDI PER SBLOCCARE IL MONDO ANIME</h2></div>", unsafe_allow_html=True)
