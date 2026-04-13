
import streamlit as st
import requests
import streamlit_authenticator as stauth

# --- 1. CONFIGURAZIONE E FIX SFONDO MANGA ---
st.set_page_config(page_title="My Anime News", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    /* SFONDO MANGA APPLICATO AL LIVELLO PIÙ PROFONDO */
    .stApp {
        background-image: url("https://wallpaperaccess.com");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }

    /* FIX: Rende trasparenti i contenitori che bloccano lo sfondo */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0) !important;
    }

    /* Velo scuro leggero per la leggibilità */
    [data-testid="stMainViewContainer"] {
        background-color: rgba(0, 0, 0, 0.5) !important;
    }
    
    /* SIDEBAR SCURA */
    [data-testid="stSidebar"] { 
        background-color: rgba(0, 0, 0, 0.85) !important; 
        border-right: 2px solid #ff4b4b; 
    }
    
    /* LOGO GIGANTE SIDEBAR */
    .logo-text {
        font-size: 42px !important;
        font-weight: 900;
        color: #ff4b4b !important;
        text-align: center;
        text-shadow: 2px 2px 10px #000;
        line-height: 1.1;
        margin-bottom: 20px;
    }

    /* CARD ANIME BIANCHE SOLIDE */
    .anime-card {
        background-color: rgba(255, 255, 255, 0.95); 
        border-radius: 15px;
        padding: 15px;
        color: #000 !important;
        border: 2px solid #ff4b4b;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
    }
    
    h1, h2, h3 { color: #ff4b4b !important; text-shadow: 2px 2px 5px #000; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SISTEMA ACCOUNT ---
if 'users' not in st.session_state:
    st.session_state['users'] = {"usernames": {"admin": {"name": "Admin", "password": "123", "email": "a@a.it"}}}

authenticator = stauth.Authenticate(st.session_state['users'], "key", "sig", cookie_expiry_days=30)

# LOGO NELLA SIDEBAR
st.sidebar.markdown('<p class="logo-text">🏮<br>MY ANIME NEWS</p>', unsafe_allow_html=True)
authenticator.login(location='sidebar')

auth_status = st.session_state.get('authentication_status')

# --- 3. LOGICA DI VISUALIZZAZIONE ---
if auth_status:
    st.sidebar.success(f"Online: {st.session_state.get('name')}")
    authenticator.logout('Logout', 'sidebar')
    st.title("🏮 DATABASE ATTIVO")
    
    categoria = st.selectbox("CATEGORIA:", ["IN CORSO", "PROSSIMAMENTE", "TOP RATED"])

    @st.cache_data(ttl=3600)
    def get_data(mode):
        urls = {"IN CORSO": "https://jikan.moe", "PROSSIMAMENTE": "https://jikan.moe", "TOP RATED": "https://jikan.moe"}
        try:
            r = requests.get(urls[mode])
            return r.json().get('data', []) if r.status_code == 200 else []
        except: return []

    data = get_data(categoria)
    if not data: data = []

    cols = st.columns(3)
    for i, anime in enumerate(data[:12]):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="anime-card">
                    <img src="{anime['images']['jpg']['large_image_url']}" style="width:100%; border-radius:10px; height:300px; object-fit:cover;">
                    <h4 style="color:#000 !important; margin-top:10px; font-weight:bold;">{anime['title'][:30]}</h4>
                    <p style="color:#444 !important;">⭐ Voto: {anime.get('score', 'N/A')}</p>
                </div>
            """, unsafe_allow_html=True)
            st.link_button("DETTAGLI", anime['url'])

else:
    # SCHERMATA INIZIALE CON IMMAGINE ANIME
    st.title("🏯 ACCEDI AL PORTALE")
    st.image("https://alphacoders.com", use_container_width=True)
    st.warning("Esegui il login nella barra laterale per consultare i file riservati.")
