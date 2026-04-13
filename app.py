import streamlit as st
import requests
import streamlit_authenticator as stauth

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="My Anime News Pro", page_icon="🏮", layout="wide")

# --- 2. STILE MARMO + NEBBIA ANIMATA ---
st.markdown("""
    <style>
    /* SFONDO MARMO NERO */
    .stApp {
        background-color: #000000;
        background-image: 
            radial-gradient(at 0% 0%, rgba(255,255,255,0.05) 0px, transparent 50%),
            radial-gradient(at 50% 0%, rgba(255,255,255,0.02) 0px, transparent 50%),
            linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(0,0,0,1) 50%, rgba(255,255,255,0.03) 100%);
        background-attachment: fixed;
    }

    /* EFFETTO NEBBIA DINAMICA */
    @keyframes fogMove {
        from { background-position: 0 0; }
        to { background-position: 10000px 5000px; }
    }
    
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: url('https://transparenttextures.com');
        opacity: 0.3;
        z-index: 0;
        pointer-events: none;
        animation: fogMove 200s linear infinite;
    }

    /* CONTENITORE CENTRALE TRASPARENTE */
    .main .block-container {
        background-color: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 40px;
        border: 1px solid rgba(255, 75, 75, 0.3);
        position: relative;
        z-index: 1;
    }

    /* LOGO GIGANTE PULSANTE */
    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
    .logo-text {
        font-size: 50px !important;
        font-weight: 900;
        color: #ff4b4b !important;
        text-align: center;
        text-shadow: 0 0 20px #ff4b4b;
        animation: pulse 2s infinite;
    }

    /* CARD ANIME */
    .anime-card {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 75, 75, 0.2);
        transition: 0.4s;
    }
    .anime-card:hover {
        border-color: #ff4b4b;
        transform: translateY(-10px);
        box-shadow: 0 10px 30px rgba(255, 75, 75, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SISTEMA ACCOUNT ---
if 'users' not in st.session_state:
    st.session_state['users'] = {"usernames": {"admin": {"name": "Admin", "password": "123", "email": "a@a.it"}}}

authenticator = stauth.Authenticate(st.session_state['users'], "anime_pro_key", "sig_key", cookie_expiry_days=30)
st.sidebar.markdown('<p class="logo-text">🏮<br>MY ANIME NEWS</p>', unsafe_allow_html=True)
authenticator.login(location='sidebar')

auth_status = st.session_state.get('authentication_status')

# --- 4. LOGICA VISUALIZZAZIONE ---
if auth_status:
    name = st.session_state.get('name')
    st.sidebar.success(f"Online: {name}")
    authenticator.logout('Logout', 'sidebar')
    
    st.title("🏮 DATABASE ATTIVO")
    cat = st.selectbox("CATEGORIA:", ["IN CORSO", "PROSSIMAMENTE", "TOP RATED"])
    url_map = {"IN CORSO": "seasons/now", "PROSSIMAMENTE": "seasons/upcoming", "TOP RATED": "top/anime"}

    try:
        res = requests.get(f"https://jikan.moe{url_map[cat]}").json().get('data', [])[:12]
        cols = st.columns(3)
        for i, anime in enumerate(res):
            with cols[i % 3]:
                st.markdown(f"""
                    <div class="anime-card">
                        <img src="{anime['images']['jpg']['large_image_url']}" style="width:100%; height:300px; object-fit:cover; border-radius:10px;">
                        <h4 style="color:#ff4b4b; margin-top:10px;">{anime['title'][:30]}</h4>
                    </div>
                """, unsafe_allow_html=True)
                st.link_button("DETTAGLI", anime['url'])
    except:
        st.error("Errore nel caricamento dei dati.")

else:
    st.title("ACCESSO PROTETTO")
    # Immagine di benvenuto (se caricata su GitHub, se no non appare nulla)
    st.image("benvenuto.jpg", use_container_width=True)
    
    with st.sidebar.expander("🆕 REGISTRATI"):
        try:
            if authenticator.register_user(location='sidebar'):
                st.success('Registrato! Accedi sopra.')
        except Exception as e:
            st.error(f"Errore: {e}")
