import streamlit as st
import requests
import streamlit_authenticator as stauth
from datetime import datetime

# --- 1. CONFIGURAZIONE & DESIGN "SAKURA CYBERPUNK" ---
st.set_page_config(page_title="My Anime News - Sakura Edition", page_icon="🌸", layout="wide")

st.markdown("""
    <style>
    @import url('https://googleapis.com');

    /* BACKGROUND & SAKURA ANIMATION */
    .stApp {
        background: #050508;
        color: #f0f0f0;
        font-family: 'Rajdhani', sans-serif;
        overflow: hidden;
    }

    /* Effetto Petali di Ciliegio */
    .sakura-container {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none;
        z-index: 0;
    }

    .petal {
        position: absolute;
        background-color: #ffb7c5;
        border-radius: 150% 0 150% 0;
        opacity: 0.7;
        animation: fall linear infinite;
    }

    @keyframes fall {
        0% { transform: translateY(-100px) rotate(0deg); opacity: 0; }
        10% { opacity: 0.8; }
        100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
    }

    /* LOGO & TITOLI */
    .anime-logo {
        font-family: 'Bangers', cursive;
        font-size: 5.5rem;
        text-align: center;
        color: #ff4b4b;
        text-shadow: 0 0 20px rgba(255, 75, 75, 0.5);
        margin: 0;
    }

    .fresche-title {
        text-align: center;
        font-size: 1.5rem;
        color: #ffb7c5;
        font-weight: 700;
        letter-spacing: 5px;
        margin-bottom: 40px;
        text-transform: uppercase;
    }

    /* CARD DESIGN */
    .fresh-card {
        background: rgba(20, 20, 30, 0.8);
        border: 2px solid rgba(255, 183, 197, 0.2);
        border-radius: 15px;
        padding: 20px;
        transition: 0.4s;
        backdrop-filter: blur(5px);
    }
    .fresh-card:hover {
        border-color: #ff4b4b;
        box-shadow: 0 0 20px rgba(255, 75, 75, 0.3);
        transform: translateY(-5px);
    }

    .fresh-badge {
        background: #ff4b4b;
        color: black;
        padding: 2px 12px;
        font-weight: 900;
        font-size: 0.8rem;
        border-radius: 5px;
    }
    </style>

    <!-- Iniezione Petali (Generati via CSS/HTML) -->
    <div class="sakura-container">
        <div class="petal" style="width:10px; height:10px; left:10%; animation-duration:10s; animation-delay:1s;"></div>
        <div class="petal" style="width:12px; height:12px; left:25%; animation-duration:12s; animation-delay:3s;"></div>
        <div class="petal" style="width:8px; height:8px; left:45%; animation-duration:8s; animation-delay:0s;"></div>
        <div class="petal" style="width:14px; height:14px; left:70%; animation-duration:15s; animation-delay:5s;"></div>
        <div class="petal" style="width:10px; height:10px; left:85%; animation-duration:11s; animation-delay:2s;"></div>
    </div>
    """, unsafe_allow_html=True)

# --- 2. SISTEMA ACCOUNT ---
if 'config' not in st.session_state:
    st.session_state['config'] = {
        "credentials": {"usernames": {"admin": {"name": "Redattore Capo", "password": "$2b$12$K7T6U/f0XpM9kPzN8Ff1.O6R5T7n5.N0v4P0E7S6Z.k6W/F7f5W2K", "email": "admin@myanimenews.it"}}},
        "cookie": {"key": "sakura_key", "name": "sakura_cookie", "expiry_days": 30}
    }

authenticator = stauth.Authenticate(
    st.session_state['config']['credentials'],
    st.session_state['config']['cookie']['name'],
    st.session_state['config']['cookie']['key'],
    st.session_state['config']['cookie']['expiry_days']
)

# --- 3. LOGICA APP ---
name, auth_status, username = authenticator.login(location='sidebar')

if auth_status:
    st.sidebar.markdown("<h1 style='text-align:center;'>🌸</h1>", unsafe_allow_html=True)
    st.sidebar.write(f"Shinobi: **{name}**")
    authenticator.logout('Logout', 'sidebar')

    # Header
    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    st.markdown('<p class="fresche-title">INFORMAZIONI ANIME FRESCHE</p>', unsafe_allow_html=True)

    # Fetch Dati (Simulazione News Fresche tramite Jikan API)
    try:
        res = requests.get("https://jikan.moe").json().get('data', [])[:9]
        cols = st.columns(3)
        for i, anime in enumerate(res):
            with cols[i % 3]:
                st.markdown(f"""
                    <div class="fresh-card">
                        <span class="fresh-badge">FRESCA</span>
                        <img src="{anime['images']['jpg']['large_image_url']}" style="width:100%; height:220px; object-fit:cover; border-radius:10px; margin: 15px 0;">
                        <h4 style="color:#ff4b4b; margin:0;">{anime['title'][:30]}</h4>
                        <p style="font-size:0.8rem; color:#888;">{anime.get('studios', [{'name':'N/D'}])[0]['name']} • {anime.get('episodes', '?')} Episodi</p>
                    </div>
                """, unsafe_allow_html=True)
                with st.expander("DETTAGLI SHINOBI"):
                    st.write(anime.get('synopsis', 'Info segrete...')[:200] + "...")
                    st.link_button("APRI SCHEDA", anime['url'], use_container_width=True)
    except:
        st.error("Errore nel caricamento del feed Sakura.")

elif auth_status is False:
    st.sidebar.error("Accesso negato.")
else:
    # Landing Page
    st.markdown("""
        <div style="text-align:center; margin-top:120px;">
            <p class="anime-logo">MY ANIME NEWS</p>
            <p style="color:#ffb7c5; letter-spacing:10px;">ACCEDI PER LE INFORMAZIONI FRESCHE</p>
            <p style="opacity:0.5;">Usa admin | 123 nel menu a lato</p>
        </div>
    """, unsafe_allow_html=True)
