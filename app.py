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

    /* FOGLIE GIGANTI ROSA NEON - VISIBILITÀ MASSIMA */
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
        filter: drop-shadow(0 0 15px #ffb7c5);
        animation: fall linear infinite;
    }
    @keyframes fall {
        0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; }
        10% { opacity: 0.8; }
        100% { transform: translateY(110vh) rotate(720deg); opacity: 0; }
    }

    /* LOGO TITANICO - MY ANIME NEWS */
    .anime-logo { 
        font-family: 'Bangers', cursive; 
        /* Dimensione aumentata drasticamente */
        font-size: clamp(8rem, 22vw, 15rem); 
        text-align: center; 
        color: #fff; 
        text-shadow: 0 0 25px #ff4b4b, 0 0 50px #ff4b4b, 0 0 100px #ff4b4b; 
        margin-top: -150px; /* Ancora più in alto */
        line-height: 0.85;
        position: relative;
        z-index: 10;
        white-space: nowrap;
    }

    /* SCRITTA SOTTO BIANCA PULITA */
    .fresche-title { 
        text-align: center; 
        font-size: clamp(1.2rem, 3.5vw, 2.5rem); 
        color: #ffffff !important; 
        font-weight: 700; 
        letter-spacing: 15px; 
        margin-top: -20px; 
        margin-bottom: 70px; 
        text-transform: uppercase;
        display: block;
        position: relative;
        z-index: 10;
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
        <div class="petal" style="width:70px; height:70px; left:5%; animation-duration:7s;"></div>
        <div class="petal" style="width:90px; height:90px; left:25%; animation-duration:12s;"></div>
        <div class="petal" style="width:60px; height:60px; left:50%; animation-duration:10s;"></div>
        <div class="petal" style="width:110px; height:110px; left:75%; animation-duration:15s;"></div>
    </div>
""", unsafe_allow_html=True)

# --- 2. SISTEMA ACCOUNT ---
if 'config' not in st.session_state:
    st.session_state.config = {
        "credentials": {
            "usernames": {
                "admin": {"name": "Capo", "password": "$2b$12$K7T6U/f0XpM9kPzN8Ff1.O6R5T7n5.N0v4P0E7S6Z.k6W/F7f5W2K", "email": "a@b.com"}
            }
        },
        "cookie": {"key": "sakura_v16_giant", "name": "man_cookie_v16", "expiry_days": 30}
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

# --- 3. NEWS & CHAT ---
@st.cache_data(ttl=600)
def get_fresh_news():
    try:
        r = requests.get("https://jikan.moe", timeout=10)
        return r.json().get('data', [])[:9] if r.status_code == 200 else []
    except: return []

# --- 4. LOGICA VISUALIZZAZIONE ---
if auth_status:
    st.sidebar.write(f"🏮 Shinobi: **{name}**")
    menu = st.sidebar.radio("SISTEMA", ["🏠 News", "💬 Chat"])
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
            st.warning("🏮 Server Jikan in caricamento...")

elif auth_status is None:
    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    st.markdown('<p class="fresche-title">INFORMAZIONI ANIME FRESCHE</p>', unsafe_allow_html=True)
    with st.sidebar.expander("Non hai un account? Registrati"):
        try:
            if authenticator.register_user(location='main'):
                st.success('Registrato! Ora fai il login.')
        except Exception as e:
            st.error(f"Errore: {e}")

    st.markdown("<div style='text-align:center;'><h3>ACCEDI DALLA SIDEBAR</h3></div>", unsafe_allow_html=True)
