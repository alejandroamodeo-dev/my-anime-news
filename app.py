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
    .sakura-container { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 9999; }
    .petal { position: absolute; background-color: #ffb7c5; border-radius: 150% 0 150% 0; opacity: 0.8; filter: drop-shadow(0 0 8px #ffb7c5); animation: fall linear infinite; }
    @keyframes fall { 0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; } 100% { transform: translateY(110vh) rotate(720deg); opacity: 0; } }
    .anime-logo { font-family: 'Bangers', cursive; font-size: clamp(6rem, 15vw, 12rem); text-align: center; color: #fff; text-shadow: 0 0 20px #ff4b4b, 0 0 40px #ff4b4b, 0 0 80px #ff4b4b; margin-top: -120px; line-height: 0.9; }
    .fresche-title { text-align: center; font-size: clamp(1rem, 3vw, 1.8rem); color: #ffffff !important; font-weight: 700; letter-spacing: 12px; margin-top: -10px; margin-bottom: 60px; text-transform: uppercase; }
    .fresh-card { background: rgba(45, 45, 50, 0.9); border: 2px solid rgba(255, 75, 75, 0.4); border-radius: 15px; padding: 25px; backdrop-filter: blur(10px); height: 500px; transition: 0.3s; }
    .fresh-card:hover { border-color: #ff4b4b; box-shadow: 0 0 30px rgba(255, 75, 75, 0.6); transform: scale(1.02); }
    </style>
    <div class="sakura-container">
        <div class="petal" style="width:40px; height:40px; left:10%; animation-duration:8s;"></div>
        <div class="petal" style="width:55px; height:55px; left:35%; animation-duration:12s;"></div>
        <div class="petal" style="width:70px; height:70px; left:80%; animation-duration:15s;"></div>
    </div>
""", unsafe_allow_html=True)

# --- 2. SISTEMA ACCOUNT ---
if 'config' not in st.session_state:
    st.session_state.config = {"credentials": {"usernames": {"admin": {"name": "Capo", "password": "$2b$12$K7T6U/f0XpM9kPzN8Ff1.O6R5T7n5.N0v4P0E7S6Z.k6W/F7f5W2K", "email": "a@b.com"}}}, "cookie": {"key": "sakura_v13", "name": "man_cookie", "expiry_days": 30}}

authenticator = stauth.Authenticate(st.session_state.config['credentials'], "man_cookie", "sakura_v13", 30)
authenticator.login(location='sidebar')
auth_status = st.session_state.get("authentication_status")
name = st.session_state.get("name")

# --- 3. LOGICA NEWS (CON RE-TRY AUTOMATICO) ---
@st.cache_data(ttl=600)
def get_fresh_news():
    urls = ["https://jikan.moe", "https://jikan.moe"]
    for url in urls:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                return r.json().get('data', [])[:9]
            time.sleep(1) # Aspetta se il server risponde male
        except: continue
    return []

# --- 4. LOGICA CHAT INTELLIGENTE ---
def get_ai_response(char, user_text):
    text = user_text.lower()
    responses = {
        "Naruto": {
            "cibo": "Il Ramen di Ichiraku è il migliore del mondo! Andiamoci insieme!",
            "combattere": "Non mi arrenderò mai! Userò il mio Rasengan per proteggere tutti!",
            "sogno": "Diventerò Hokage, costi quel che costi! È la mia strada ninja!",
            "default": "Dattebayo! Sei un tipo in gamba, continuiamo ad allenarci!"
        },
        "Gojo": {
            "forte": "Tranquillo, io sono letteralmente l'apice della forza. L'Infinito è tra noi.",
            "cibo": "Hai dei dolcetti? Adoro lo zucchero, mi aiuta a pensare meglio.",
            "paura": "Non c'è nulla di cui aver paura quando ci sono io qui. Sei al sicuro.",
            "default": "Mmm, interessante... ma ora godiamoci la vista, okay?"
        }
    }
    char_data = responses.get(char, responses["Naruto"])
    for key in char_data:
        if key in text: return char_data[key]
    return char_data["default"]

# --- 5. APP LOGIC ---
if auth_status:
    st.sidebar.write(f"🏮 Shinobi: **{name}**")
    menu = st.sidebar.radio("SISTEMA", ["🏠 News Fresche", "💬 AI Chat Personaggi", "📊 Mega Sondaggio"])
    authenticator.logout('Logout', 'sidebar')

    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    st.markdown('<p class="fresche-title">INFORMAZIONI ANIME FRESCHE</p>', unsafe_allow_html=True)

    if menu == "🏠 News Fresche":
        news_data = get_fresh_news()
        if news_data:
            cols = st.columns(3)
            for i, anime in enumerate(news_data):
                with cols[i % 3]:
                    st.markdown(f"""<div class="fresh-card">
                        <img src="{anime['images']['jpg']['large_image_url']}" style="width:100%; height:250px; object-fit:cover; border-radius:10px;">
                        <h4 style="color:#ff4b4b; margin-top:10px;">{anime.get('title', 'N/D')[:35]}</h4>
                        <p style="color:#ccc; font-size:0.9rem;">⭐ Score: {anime.get('score', 'N/A')}</p>
                    </div>""", unsafe_allow_html=True)
        else:
            st.error("🏮 I server Jikan sono carichi. Ho attivato il recupero automatico, prova a ricaricare tra un istante.")

    elif menu == "💬 AI Chat Personaggi":
        char = st.selectbox("Scegli con chi parlare:", ["Naruto", "Gojo"])
        if "chat_history" not in st.session_state: st.session_state.chat_history = []
        
        user_input = st.chat_input(f"Invia un messaggio a {char}...")
        if user_input:
            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("assistant", get_ai_response(char, user_input)))
        
        for role, text in st.session_state.chat_history[-6:]:
            st.chat_message(role).write(text)

elif auth_status is None:
    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    with st.sidebar.expander("Non hai un account? Registrati"):
        # FIX TYPERROR: Rimosso parametro preauthorization per compatibilità universale
        if authenticator.register_user(location='main'):
            st.success('Registrato! Effettua il login ora.')

    st.markdown("<div style='text-align:center;'><h2>SBLOCCA IL DATABASE DALLA SIDEBAR</h2></div>", unsafe_allow_html=True)
