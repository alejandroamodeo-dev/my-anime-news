import streamlit as st
import requests
import streamlit_authenticator as stauth
import json
import os

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="My Anime News Pro", page_icon="🏮", layout="wide")

# --- 2. STILE CHIARO/MODERNO (GRIGIO ANTRACITE + NEBBIA) ---
st.markdown("""
    <style>
    /* SFONDO GRIGIO ANTRACITE (PIÙ CHIARO DEL NERO) */
    .stApp {
        background-color: #1e2124; /* Grigio scuro ma non nero */
        background-image: 
            radial-gradient(at 0% 0%, rgba(255,255,255,0.1) 0px, transparent 50%),
            radial-gradient(at 50% 100%, rgba(255,75,75,0.05) 0px, transparent 50%),
            linear-gradient(180deg, #1e2124 0%, #2f3136 100%);
        background-attachment: fixed;
    }

    /* NEBBIA PIÙ VISIBILE */
    @keyframes fogMove {
        from { background-position: 0 0; }
        to { background-position: 10000px 5000px; }
    }
    
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: url('https://transparenttextures.com');
        opacity: 0.4; /* Aumentata opacità per vederla meglio */
        z-index: 0;
        pointer-events: none;
        animation: fogMove 180s linear infinite;
    }

    /* CONTENITORE CENTRALE CON VETRO SFOCATO */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    .main .block-container {
        background-color: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px); /* Effetto vetro più forte */
        border-radius: 25px;
        padding: 40px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        z-index: 1;
    }

    /* LOGO SIDEBAR */
    .logo-text {
        font-size: 42px !important;
        font-weight: 900;
        color: #ff4b4b !important;
        text-align: center;
        text-shadow: 2px 2px 15px rgba(255, 75, 75, 0.3);
    }

    /* CARD ANIME PIÙ CHIARE */
    .anime-card {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: 0.3s;
    }
    .anime-card:hover {
        background-color: rgba(255, 255, 255, 0.15);
        border-color: #ff4b4b;
        transform: translateY(-5px);
    }
    
    h1, h2, h3 { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SISTEMA ACCOUNT ---
if 'users' not in st.session_state:
    st.session_state['users'] = {
        "usernames": {
            "admin": {"name": "Admin", "password": "123", "email": "admin@anime.it"}
        }
    }

authenticator = stauth.Authenticate(st.session_state['users'], "anime_pro_v3", "signature", cookie_expiry_days=30)
st.sidebar.markdown('<p class="logo-text">🏮<br>MY ANIME NEWS</p>', unsafe_allow_html=True)
authenticator.login(location='sidebar')

auth_status = st.session_state.get('authentication_status')
name = st.session_state.get('name')

# --- 4. LOGICA VISUALIZZAZIONE ---
if auth_status:
    st.sidebar.success(f"Online: {name}")
    authenticator.logout('Logout', 'sidebar')
    
    st.title("🏮 NOTIZIE RECENTI")
    categoria = st.selectbox("FILTRA PER:", ["IN CORSO", "PROSSIMAMENTE", "TOP RATED"])
    
    url_map = {
        "IN CORSO": "https://jikan.moe",
        "PROSSIMAMENTE": "https://jikan.moe",
        "TOP RATED": "https://jikan.moe"
    }

    try:
        r = requests.get(url_map[categoria])
        data = r.json().get('data', [])[:12] if r.status_code == 200 else []
            
        if data:
            cols = st.columns(3)
            for i, anime in enumerate(data):
                with cols[i % 3]:
                    st.markdown(f'<div class="anime-card"><img src="{anime["images"]["jpg"]["large_image_url"]}" style="width:100%; height:300px; object-fit:cover; border-radius:10px;"><h4 style="color:#ff4b4b; margin-top:10px;">{anime["title"][:30]}</h4></div>', unsafe_allow_html=True)
                    st.link_button("APRI SCHEDA", anime['url'])
        else:
            st.warning("⚠️ Database momentaneamente occupato.")
    except:
        st.error("Connessione fallita.")

else:
    st.title("🏯 ACCESSO AL DATABASE")
    
    try:
        st.image("benvenuto.jpg", use_container_width=True)
    except:
        st.markdown('<div style="background: #2f3136; padding: 80px; border-radius: 20px; text-align: center; border: 1px solid #ff4b4b;"><h1 style="color: #ff4b4b !important;">MY ANIME NEWS</h1><p style="color: white;">Inserisci i file di accesso</p></div>', unsafe_allow_html=True)
    
    with st.sidebar.expander("🆕 REGISTRATI"):
        try:
            if authenticator.register_user(location='sidebar', pre_authorization=[]):
                st.success('Registrato! Accedi ora.')
        except Exception as e:
            st.error(f"Errore: {e}")
    
    st.warning("Accedi dalla barra laterale per sbloccare i contenuti.")
