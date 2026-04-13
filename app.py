import streamlit as st
import requests
import streamlit_authenticator as stauth
from datetime import datetime

# --- 1. CONFIGURAZIONE & STILE "ANIME TECH" ---
st.set_page_config(page_title="My Anime News - Fresh Info", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    @import url('https://googleapis.com');

    /* BACKGROUND STILE NOTTE A TOKYO */
    .stApp {
        background: #020205;
        background-image: 
            linear-gradient(rgba(255, 75, 75, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 75, 75, 0.05) 1px, transparent 1px);
        background-size: 30px 30px;
        color: #f0f0f0;
        font-family: 'Rajdhani', sans-serif;
    }

    /* LOGO ANIME STYLE */
    .anime-logo {
        font-family: 'Bangers', cursive;
        font-size: 5rem;
        text-align: center;
        color: #ff4b4b;
        text-shadow: 4px 4px 0px #5a0000, 0 0 20px rgba(255, 75, 75, 0.6);
        margin-bottom: 0px;
        letter-spacing: 2px;
    }

    .japanese-text {
        font-family: 'Noto Sans JP', sans-serif;
        text-align: center;
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.3);
        margin-bottom: 40px;
        text-transform: uppercase;
    }

    /* CARD "FRESCHE" CON BORDO NEON */
    .fresh-card {
        background: rgba(15, 15, 25, 0.9);
        border: 2px solid #222;
        border-radius: 0px 20px 0px 20px; /* Taglio stile anime */
        padding: 20px;
        transition: 0.4s ease;
        position: relative;
        overflow: hidden;
    }

    .fresh-card:hover {
        border-color: #ff4b4b;
        box-shadow: 0 0 25px rgba(255, 75, 75, 0.4);
        transform: skewX(-2deg); /* Effetto dinamico */
    }

    .fresh-tag {
        background: #ff4b4b;
        color: black;
        padding: 2px 15px;
        font-weight: 900;
        font-family: 'Bangers', cursive;
        font-size: 1rem;
        clip-path: polygon(0 0, 100% 0, 85% 100%, 0% 100%);
    }

    .anime-title {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        font-size: 1.4rem;
        color: #fff;
        margin-top: 15px;
        text-transform: uppercase;
    }

    /* SIDEBAR STYLE */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #100000 0%, #050505 100%) !important;
        border-right: 2px solid #ff4b4b;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SISTEMA ACCOUNT ---
if 'config' not in st.session_state:
    st.session_state['config'] = {
        "credentials": {"usernames": {"admin": {"name": "Otaku Admin", "password": "$2b$12$K7T6U/f0XpM9kPzN8Ff1.O6R5T7n5.N0v4P0E7S6Z.k6W/F7f5W2K", "email": "info@myanimenews.it"}}},
        "cookie": {"key": "man_key", "name": "man_cookie", "expiry_days": 30}
    }

authenticator = stauth.Authenticate(
    st.session_state['config']['credentials'],
    st.session_state['config']['cookie']['name'],
    st.session_state['config']['cookie']['key'],
    st.session_state['config']['cookie']['expiry_days']
)

# --- 3. FETCH INFO ANIME ---
@st.cache_data(ttl=300)
def get_fresh_info():
    try:
        r = requests.get("https://jikan.moe")
        return r.json().get('data', [])[:12]
    except:
        return []

# --- 4. INTERFACCIA ---
name, auth_status, username = authenticator.login(location='sidebar')

if auth_status:
    # Sidebar
    st.sidebar.markdown("<h1 style='color:#ff4b4b; text-align:center;'>🏮</h1>", unsafe_allow_html=True)
    st.sidebar.title("MENU UTENTE")
    st.sidebar.write(f"Shinobi Online: **{name}**")
    authenticator.logout('Log Out', 'sidebar')

    # Header
    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    st.markdown('<p class="japanese-text">最新のアニメ情報 — INFORMAZIONI ANIME FRESCHE</p>', unsafe_allow_html=True)
    
    # Grid News
    data = get_fresh_info()
    
    if data:
        cols = st.columns(3)
        for idx, anime in enumerate(data):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="fresh-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span class="fresh-tag">FRESCA</span>
                            <span style="color:#ff4b4b; font-weight:bold;">#{idx+1}</span>
                        </div>
                        <img src="{anime['images']['jpg']['large_image_url']}" style="width:100%; height:250px; object-fit:cover; border-radius:5px; margin-top:10px; border-bottom: 3px solid #ff4b4b;">
                        <div class="anime-title">{anime['title'][:35]}</div>
                        <p style="color:#888; font-size:0.85rem;">Status: {anime.get('status', 'In corso')}<br>Studio: {anime.get('studios', [{'name': 'N/D'}])[0]['name']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                with st.expander("SCOPRI DI PIÙ"):
                    st.write(f"**Trama:** {anime.get('synopsis', 'Info in arrivo...')[:300]}...")
                    st.link_button("VEDI TRAILER", anime['url'], use_container_width=True)
    else:
        st.error("⚠️ Errore nel caricamento delle info fresche. Riprova.")

elif auth_status is False:
    st.sidebar.error("Chiave d'accesso errata.")
else:
    # Landing stile Anime
    st.markdown("""
        <div style="text-align:center; margin-top:80px;">
            <p class="anime-logo" style="font-size:6rem;">MY ANIME NEWS</p>
            <p class="japanese-text" style="letter-spacing:15px;">LOGIN REQUIRED</p>
            <div style="background: rgba(255,75,75,0.1); border: 2px dashed #ff4b4b; padding: 40px; display: inline-block; border-radius: 20px;">
                <h3 style="color:white; margin:0;">ACCEDI PER LE INFO FRESCHE</h3>
                <p style="color:#666;">Usa le credenziali nel menu a sinistra</p>
                <code style="background:white; color:black; padding:5px 10px; border-radius:5px;">admin | 123</code>
            </div>
        </div>
    """, unsafe_allow_html=True)
