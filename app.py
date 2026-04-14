import streamlit as st
import requests
import streamlit_authenticator as stauth
from datetime import datetime

# --- 1. DESIGN "ULTRA TITAN" OTTIMIZZATO ---
st.set_page_config(page_title="My Anime News - Kitsu Edition", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    .stApp { background: #050508; color: #f0f0f0; font-family: 'Rajdhani', sans-serif; }

    /* PETALI SAKURA - LEGGERI E VELOCI */
    .sakura-container { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 99999; }
    .petal { position: absolute; background-color: #ffb7c5; border-radius: 150% 0 150% 0; opacity: 0.8; filter: drop-shadow(0 0 10px #ffb7c5); animation: fall linear infinite; }
    @keyframes fall { 0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; } 100% { transform: translateY(110vh) rotate(720deg); opacity: 0; } }

    /* TITOLO TITANICO */
    .anime-logo { 
        font-family: 'Bangers', cursive; font-size: clamp(8rem, 25vw, 15rem); 
        text-align: center; color: #fff; text-shadow: 0 0 20px #ff4b4b, 0 0 40px #ff4b4b; 
        margin-top: -140px; line-height: 0.8; position: relative; z-index: 10;
    }

    .fresche-title { 
        text-align: center; font-size: clamp(1rem, 3vw, 1.8rem); color: #ffffff !important; 
        font-weight: 700; letter-spacing: 12px; margin-top: -10px; margin-bottom: 70px; 
        text-transform: uppercase; display: block; position: relative; z-index: 10; opacity: 0.9;
    }

    .fresh-card { 
        background: rgba(45, 45, 50, 0.9); border: 2px solid rgba(255, 75, 75, 0.4); 
        border-radius: 15px; padding: 20px; backdrop-filter: blur(10px); height: 500px; 
    }
    </style>

    <div class="sakura-container">
        <div class="petal" style="width:50px; height:50px; left:10%; animation-duration:10s;"></div>
        <div class="petal" style="width:80px; height:80px; left:30%; animation-duration:15s;"></div>
        <div class="petal" style="width:100px; height:100px; left:70%; animation-duration:12s;"></div>
    </div>
""", unsafe_allow_html=True)

# --- 2. SISTEMA ACCOUNT ---
if 'config' not in st.session_state:
    st.session_state.config = {
        "credentials": {"usernames": {"admin": {"name": "Redattore Capo", "password": "$2b$12$K7T6U/f0XpM9kPzN8Ff1.O6R5T7n5.N0v4P0E7S6Z.k6W/F7f5W2K", "email": "admin@myanimenews.it"}}},
        "cookie": {"key": "sakura_v24_kitsu", "name": "man_cookie_v24", "expiry_days": 30}
    }

authenticator = stauth.Authenticate(st.session_state.config['credentials'], st.session_state.config['cookie']['name'], st.session_state.config['cookie']['key'], st.session_state.config['cookie']['expiry_days'])
authenticator.login(location='sidebar')
auth_status = st.session_state.get("authentication_status")
name = st.session_state.get("name")

# --- 3. NUOVO MOTORE NEWS (KITSU API - SUPER FAST) ---
@st.cache_data(ttl=1800)
def get_kitsu_news():
    url = "https://kitsu.io[status]=current&page[limit]=9&sort=-userCount"
    try:
        response = requests.get(url, timeout=10)
        return response.json()['data']
    except:
        return []

# --- 4. LOGICA VISUALIZZAZIONE ---
if auth_status:
    st.sidebar.write(f"🏮 Shinobi: **{name}**")
    menu = st.sidebar.radio("SISTEMA", ["🏠 News", "💬 Chat"])
    authenticator.logout('Logout', 'sidebar')

    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    st.markdown('<p class="fresche-title">INFORMAZIONI ANIME FRESCHE</p>', unsafe_allow_html=True)

    if menu == "🏠 News":
        news = get_kitsu_news()
        if news:
            cols = st.columns(3)
            for i, a in enumerate(news):
                attr = a['attributes']
                with cols[i % 3]:
                    st.markdown(f"""<div class="fresh-card">
                        <img src="{attr['posterImage']['large']}" style="width:100%; height:280px; object-fit:cover; border-radius:10px;">
                        <h4 style="color:#ff4b4b; margin-top:10px;">{attr['canonicalTitle'][:35]}</h4>
                        <p style="color:#ccc;">⭐ Rating: {attr['averageRating']}%</p>
                        <p style="font-size:0.8rem; color:#888;">{attr['synopsis'][:150]}...</p>
                    </div>""", unsafe_allow_html=True)
        else:
            st.error("🏮 Errore Critico: Il database Kitsu non risponde. Controlla la connessione internet.")

elif auth_status is None:
    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    st.markdown('<p class="fresche-title">INFORMAZIONI ANIME FRESCHE</p>', unsafe_allow_html=True)
    with st.sidebar.expander("Non hai un account? Registrati"):
        if authenticator.register_user(location='main'):
            st.success('Registrato! Accedi ora.')
