import streamlit as st
import requests
import streamlit_authenticator as stauth
from datetime import datetime

# --- 1. CONFIGURAZIONE & DESIGN "SAKURA ENHANCED" ---
st.set_page_config(page_title="My Anime News - Sakura HD", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    @import url('https://googleapis.com');

    /* BACKGROUND & ANIMAZIONE PETALI PIÙ GRANDI */
    .stApp {
        background: #050508;
        color: #f0f0f0;
        font-family: 'Rajdhani', sans-serif;
    }

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

    .anime-logo {
        font-family: 'Bangers', cursive;
        font-size: 6.5rem;
        text-align: center;
        color: #ff4b4b;
        text-shadow: 0 0 30px rgba(255, 75, 75, 0.6);
        margin: 10px 0;
    }

    .fresche-title {
        text-align: center;
        font-size: 2rem;
        color: #ffb7c5;
        font-weight: 700;
        letter-spacing: 8px;
        margin-bottom: 50px;
        text-transform: uppercase;
        text-shadow: 0 0 10px rgba(255, 183, 197, 0.4);
    }

    .fresh-card {
        background: rgba(20, 20, 30, 0.85);
        border: 2px solid rgba(255, 183, 197, 0.2);
        border-radius: 15px;
        padding: 25px;
        transition: 0.4s;
        backdrop-filter: blur(8px);
    }
    
    .anime-title-text {
        font-size: 1.6rem;
        font-weight: 700;
        color: #ff4b4b;
        margin-top: 10px;
    }

    .anime-info-text {
        font-size: 1.1rem;
        color: #ccc;
    }
    </style>

    <div class="sakura-container">
        <div class="petal" style="width:20px; height:20px; left:5%; animation-duration:8s;"></div>
        <div class="petal" style="width:28px; height:28px; left:20%; animation-duration:12s;"></div>
        <div class="petal" style="width:22px; height:22px; left:45%; animation-duration:10s;"></div>
        <div class="petal" style="width:30px; height:30px; left:70%; animation-duration:15s;"></div>
        <div class="petal" style="width:20px; height:20px; left:90%; animation-duration:11s;"></div>
    </div>
    """, unsafe_allow_html=True)

# --- 2. SISTEMA ACCOUNT ---
if 'config' not in st.session_state:
    st.session_state['config'] = {
        "credentials": {
            "usernames": {
                "admin": {
                    "name": "Redattore Capo", 
                    "password": "$2b$12$K7T6U/f0XpM9kPzN8Ff1.O6R5T7n5.N0v4P0E7S6Z.k6W/F7f5W2K", 
                    "email": "admin@myanimenews.it"
                }
            }
        },
        "cookie": {"key": "sakura_pro_key", "name": "sakura_cookie", "expiry_days": 30}
    }

authenticator = stauth.Authenticate(
    st.session_state['config']['credentials'],
    st.session_state['config']['cookie']['name'],
    st.session_state['config']['cookie']['key'],
    st.session_state['config']['cookie']['expiry_days']
)

# --- 3. LOGIN & REGISTRAZIONE ---
name, auth_status, username = authenticator.login(location='sidebar')

if auth_status:
    st.sidebar.markdown("<h1 style='text-align:center;'>🏮</h1>", unsafe_allow_html=True)
    st.sidebar.markdown(f"### Shinobi: **{name}**")
    authenticator.logout('Esci dal Database', 'sidebar')

    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    st.markdown('<p class="fresche-title">INFORMAZIONI ANIME FRESCHE</p>', unsafe_allow_html=True)

    try:
        # Chiamata API v4 con controllo errori robusto
        response = requests.get("https://jikan.moe", timeout=10)
        res = response.json().get('data', [])[:9]
        
        if res:
            cols = st.columns(3)
            for i, anime in enumerate(res):
                with cols[i % 3]:
                    # Estrazione sicura del nome dello studio
                    studios = anime.get('studios', [])
                    studio_name = studios[0].get('name', 'N/D') if studios else 'N/D'
                    
                    st.markdown(f"""
                        <div class="fresh-card">
                            <img src="{anime['images']['jpg']['large_image_url']}" style="width:100%; height:280px; object-fit:cover; border-radius:10px;">
                            <div class="anime-title-text">{anime['title'][:30]}</div>
                            <p class="anime-info-text">{studio_name} • {anime.get('episodes', '?')} Ep.</p>
                        </div>
                    """, unsafe_allow_html=True)
                    with st.expander("SCROLL INFORMAZIONI"):
                        st.write(f"**Trama:** {anime.get('synopsis', 'Info segrete...')[:250]}...")
                        st.link_button("COLLEGAMENTO FONTE", anime['url'], use_container_width=True)
        else:
            st.warning("🏮 Database in aggiornamento... Riprova tra un istante.")
            
    except Exception as e:
        st.error(f"Errore di sincronizzazione: {e}")

elif auth_status is False:
    st.sidebar.error("Credenziali respinte.")

# SEZIONE REGISTRAZIONE (FIXATA)
if not auth_status:
    with st.sidebar.expander("Non hai un account? Registrati"):
        try:
            # Parametro corretto pre_authorization per le ultime versioni
            if authenticator.register_user(location='main', pre_authorization=[]):
                st.success('Registrazione completata! Effettua il login dal pannello laterale.')
        except Exception as e:
            st.error(f"Errore: {e}")

    st.markdown("""
        <div style="text-align:center; margin-top:150px;">
            <p class="anime-logo" style="font-size:7rem;">MY ANIME NEWS</p>
            <p style="color:#ffb7c5; font-size:1.5rem; letter-spacing:12px;">ACCESSO RISERVATO</p>
            <p style="opacity:0.6; font-size:1.2rem;">Sblocca le Informazioni Fresche dal pannello laterale</p>
        </div>
