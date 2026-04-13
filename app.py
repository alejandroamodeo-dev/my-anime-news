
import streamlit as st
import requests
import streamlit_authenticator as stauth
import json
import os
from datetime import datetime

# --- 1. CONFIGURAZIONE E ANIMAZIONI CSS AVANZATE ---
st.set_page_config(page_title="My Anime News Pro", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    /* SFONDO MANGA CON ANIMAZIONE SOFT ZOOM */
    @keyframes slowZoom {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .stApp {
        background-image: url("https://imgur.com");
        background-size: cover;
        background-attachment: fixed;
        animation: slowZoom 30s infinite ease-in-out;
    }

    /* TRASPARENZA LIVELLI E SFOCATURA (BLUR EFFECT) */
    [data-testid="stAppViewContainer"] { background-color: rgba(0, 0, 0, 0.4) !important; }
    [data-testid="stHeader"] { background: transparent !important; }
    
    .main .block-container {
        background: rgba(0, 0, 0, 0.75);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 40px;
        border: 1px solid rgba(255, 75, 75, 0.3);
        box-shadow: 0 0 30px rgba(255, 75, 75, 0.2);
    }

    /* LOGO GIGANTE ANIMATO */
    @keyframes glow {
        from { text-shadow: 0 0 10px #ff4b4b; }
        to { text-shadow: 0 0 30px #ff4b4b, 0 0 40px #ff0000; }
    }
    .logo-text {
        font-size: 55px !important;
        font-weight: 900;
        color: #ff4b4b !important;
        text-align: center;
        animation: glow 2s infinite alternate;
        line-height: 1.1;
    }

    /* CARD ANIME CON EFFETTO HOVER */
    .anime-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .anime-card:hover {
        background: rgba(255, 75, 75, 0.1);
        border-color: #ff4b4b;
        transform: translateY(-15px) scale(1.05);
        box-shadow: 0 20px 40px rgba(255, 75, 75, 0.3);
    }

    /* CHAT BOX */
    .chat-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 20px;
        height: 400px;
        overflow-y: auto;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTIONE DATABASE LOCALE (FILE JSON) ---
def handle_data(file, data=None):
    if data is None:
        if not os.path.exists(file): return []
        with open(file, "r") as f: return json.load(f)
    else:
        with open(file, "w") as f: json.dump(data, f)

# --- 3. SISTEMA DI AUTENTICAZIONE ---
if 'users' not in st.session_state:
    st.session_state['users'] = {"usernames": {"admin": {"name": "Admin", "password": "123", "email": "a@a.it"}}}

authenticator = stauth.Authenticate(st.session_state['users'], "anime_pro_cookie", "signature_key", cookie_expiry_days=30)

st.sidebar.markdown('<p class="logo-text">🏮<br>MY ANIME NEWS</p>', unsafe_allow_html=True)
authenticator.login(location='sidebar')

auth_status = st.session_state.get('authentication_status')

# --- 4. INTERFACCIA PRINCIPALE ---
if auth_status:
    st.sidebar.success(f"Loggato come: {st.session_state.get('name')}")
    authenticator.logout('Esci dal Database', 'sidebar')
    
    # Navigazione interna
    menu = st.tabs(["📺 NOTIZIE & DATABASE", "💬 CHAT COMMUNITY", "🌟 VALUTAZIONI"])

    # --- TAB 1: NEWS ---
    with menu[0]:
        st.title("🏮 DATABASE ATTIVO")
        cat = st.selectbox("SETTORE:", ["IN CORSO", "PROSSIMAMENTE", "I MIGLIORI"])
        url_map = {"IN CORSO": "seasons/now", "PROSSIMAMENTE": "seasons/upcoming", "I MIGLIORI": "top/anime"}
        
        try:
            res = requests.get(f"https://jikan.moe{url_map[cat]}").json().get('data', [])[:12]
            cols = st.columns(3)
            for i, anime in enumerate(res):
                with cols[i % 3]:
                    st.markdown(f"""
                        <div class="anime-card">
                            <img src="{anime['images']['jpg']['large_image_url']}" style="width:100%; border-radius:15px; height:350px; object-fit:cover;">
                            <h4 style="margin-top:15px; color:#ff4b4b;">{anime['title'][:30]}...</h4>
                            <p style="color:#00ff41;">⭐ Score: {anime.get('score', 'N/A')}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.link_button("APRI SCHEDA", anime['url'])
                    st.write("")
        except: st.error("Errore di connessione al database API.")

    # --- TAB 2: CHAT ---
    with menu[1]:
        st.title("💬 CHAT IN TEMPO REALE")
        chat_history = handle_data("chat_pro.json")
        
        chat_html = "".join([f"<div style='margin-bottom:10px;'><b>{m['u']}</b> <span style='font-size:10px; color:#888;'>{m['t']}</span><br>{m['msg']}</div>" for m in chat_history[-20:]])
        st.markdown(f'<div class="chat-container">{chat_html}</div>', unsafe_allow_html=True)
        
        with st.form("chat_input", clear_on_submit=True):
            user_msg = st.text_input("Inserisci un messaggio...")
            if st.form_submit_button("Invia 🚀") and user_msg:
                chat_history.append({"u": st.session_state.get('name'), "t": datetime.now().strftime("%H:%M"), "msg": user_msg})
                handle_data("chat_pro.json", chat_history)
                st.rerun()

    # --- TAB 3: VALUTAZIONI ---
    with menu[2]:
        st.title("🌟 AREA RECENSIONI")
        st.write("Vota gli anime che hai visto nella sezione News per vederli apparire qui (Coming Soon).")

else:
    # SCHERMATA DI BENVENUTO (ANIMATA)
    st.title("🏯 ACCESSO PROTETTO")
    st.image("https://imgur.com", caption="Database My Anime News - Restricted Access", use_container_width=True)
    
    with st.sidebar.expander("🆕 NON HAI UN ACCOUNT? REGISTRATI"):
        try:
            if authenticator.register_user(location='sidebar'):
                st.success('Registrato! Ora puoi accedere.')
        except Exception as e: st.error(f"Errore: {e}")
    
    st.warning("Per favore, effettua il login nella barra laterale per consultare i file riservati.")
