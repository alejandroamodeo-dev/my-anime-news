import streamlit as st
import requests
import streamlit_authenticator as stauth
import json
import os

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="My Anime News Pro", page_icon="🏮", layout="wide")

# --- 2. STILE ULTRA DARK + NEBBIA + MARMO ---
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        background-image: 
            radial-gradient(at 0% 0%, rgba(255,255,255,0.05) 0px, transparent 50%),
            radial-gradient(at 50% 0%, rgba(255,255,255,0.02) 0px, transparent 50%),
            linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(0,0,0,1) 50%, rgba(255,255,255,0.03) 100%);
        background-attachment: fixed;
    }

    @keyframes fogMove {
        from { background-position: 0 0; }
        to { background-position: 10000px 5000px; }
    }
    
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: url('https://transparenttextures.com');
        opacity: 0.25;
        z-index: 0;
        pointer-events: none;
        animation: fogMove 250s linear infinite;
    }

    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    .main .block-container {
        background-color: rgba(0, 0, 0, 0.75);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 40px;
        border: 1px solid rgba(255, 75, 75, 0.3);
        position: relative;
        z-index: 1;
    }

    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
    .logo-text {
        font-size: 45px !important;
        font-weight: 900;
        color: #ff4b4b !important;
        text-align: center;
        text-shadow: 0 0 20px #ff4b4b;
        animation: pulse 2s infinite;
        line-height: 1.1;
    }

    .anime-card {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 75, 75, 0.2);
    }
    
    h1, h2, h3 { color: #ff4b4b !important; }
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

# --- 4. LOGICA DI VISUALIZZAZIONE ---
if auth_status:
    st.sidebar.success(f"ONLINE: {name}")
    authenticator.logout('Logout', 'sidebar')
    
    st.title("🏮 DATABASE NEWS ATTIVO")
    categoria = st.selectbox("SCEGLI CATEGORIA:", ["IN CORSO", "PROSSIMAMENTE", "TOP RATED"])
    
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
                    st.markdown(f'<div class="anime-card"><img src="{anime["images"]["jpg"]["large_image_url"]}" style="width:100%; height:300px; object-fit:cover; border-radius:10px;"><h4 style="color:#ff4b4b; margin-top:10px;">{anime["title"][:30]}...</h4></div>', unsafe_allow_html=True)
                    st.link_button("APRI FILE", anime['url'])
        else:
            st.warning("⚠️ API in sovraccarico.")
    except:
        st.error("Errore di connessione.")

else:
    st.title("🏯 ACCESSO PROTETTO")
    
    try:
        st.image("benvenuto.jpg", use_container_width=True)
    except:
        st.markdown('<div style="background: linear-gradient(90deg, #ff4b4b, #8e44ad); padding: 80px; border-radius: 20px; text-align: center;"><h1 style="color: white !important;">MY ANIME NEWS</h1></div>', unsafe_allow_html=True)
    
    with st.sidebar.expander("🆕 NON HAI UN ACCOUNT? REGISTRATI"):
        try:
            # FIX: Aggiunto pre-authorization=[] per risolvere l'errore
            if authenticator.register_user(location='sidebar', pre_authorization=[]):
                st.success('Registrato! Accedi sopra.')
        except Exception as e:
            st.error(f"Errore: {e}")
    
    st.warning("IDENTIFICARSI NELLA SIDEBAR PER SBLOCCARE I FILE.")
