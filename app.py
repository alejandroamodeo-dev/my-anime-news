
import streamlit as st
import requests
import streamlit_authenticator as stauth
import json
import os
from datetime import datetime

# --- 1. CONFIGURAZIONE E STILE ---
st.set_page_config(page_title="My Anime News & Chat", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    .stApp { background-image: url("https://imgur.com"); background-size: cover; background-attachment: fixed; }
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMainViewContainer"] { background-color: rgba(0, 0, 0, 0) !important; }
    .main .block-container { background-color: rgba(0, 0, 0, 0.7); border-radius: 20px; padding: 30px; margin-top: 20px; color: white; }
    [data-testid="stSidebar"] { background-color: rgba(0, 0, 0, 0.9) !important; border-right: 2px solid #ff4b4b; }
    .logo-text { font-size: 42px !important; font-weight: 900; color: #ff4b4b !important; text-align: center; text-shadow: 3px 3px 10px #000; line-height: 1.1; }
    .anime-card { background-color: white; border-radius: 15px; padding: 15px; color: #000 !important; border: 2px solid #ff4b4b; margin-bottom: 10px; }
    .chat-box { background-color: rgba(255,255,255,0.1); border-radius: 10px; padding: 15px; height: 300px; overflow-y: auto; border: 1px solid #ff4b4b; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FUNZIONI PER CHAT E COMMENTI (DATABASE SEMPLICE) ---
def load_data(filename, default_val):
    if not os.path.exists(filename): return default_val
    with open(filename, "r") as f: return json.load(f)

def save_data(filename, data):
    with open(filename, "w") as f: json.dump(data, f)

# --- 3. SISTEMA ACCOUNT ---
if 'users' not in st.session_state:
    st.session_state['users'] = {"usernames": {"admin": {"name": "Admin", "password": "123", "email": "a@a.it"}}}

authenticator = stauth.Authenticate(st.session_state['users'], "key", "sig", cookie_expiry_days=30)
st.sidebar.markdown('<p class="logo-text">🏮<br>MY ANIME NEWS</p>', unsafe_allow_html=True)
authenticator.login(location='sidebar')

auth_status = st.session_state.get('authentication_status')

# --- 4. LOGICA DI VISUALIZZAZIONE ---
if auth_status:
    name = st.session_state.get('name')
    st.sidebar.success(f"Online: {name}")
    authenticator.logout('Logout', 'sidebar')
    
    # --- TABS: NEWS / CHAT / COMMUNITY ---
    tab1, tab2 = st.tabs(["📺 NEWS & DATABASE", "💬 COMMUNITY CHAT"])

    with tab1:
        st.title("🏮 DATABASE ATTIVO")
        categoria = st.selectbox("CATEGORIA:", ["IN CORSO", "PROSSIMAMENTE", "TOP RATED"])
        
        # Carica News
        r = requests.get(f"https://jikan.moe{'seasons/now' if categoria=='IN CORSO' else 'seasons/upcoming' if categoria=='PROSSIMAMENTE' else 'top/anime'}")
        data = r.json().get('data', [])[:9]

        cols = st.columns(3)
        for i, anime in enumerate(data):
            with cols[i % 3]:
                st.markdown(f'<div class="anime-card"><img src="{anime["images"]["jpg"]["large_image_url"]}" style="width:100%; height:250px; object-fit:cover; border-radius:10px;"><h4 style="color:black;">{anime["title"][:25]}</h4></div>', unsafe_allow_html=True)
                
                # Valutazione e Commento per singolo Anime
                rating = st.slider(f"Voto per {anime['title'][:15]}", 1, 10, 5, key=f"rate_{anime['mal_id']}")
                commento = st.text_input(f"Commento", key=f"comm_{anime['mal_id']}")
                if st.button(f"Invia recensione", key=f"btn_{anime['mal_id']}"):
                    st.toast(f"Hai dato {rating}/10 a {anime['title']}!")

    with tab2:
        st.title("💬 GLOBAL CHAT")
        messages = load_data("chat.json", [])
        
        # Box messaggi
        chat_html = ""
        for m in messages[-20:]: # Mostra ultimi 20
            chat_html += f"<p style='margin-bottom:5px;'><b>{m['user']}</b> [{m['time']}]: {m['text']}</p>"
        st.markdown(f'<div class="chat-box">{chat_html}</div>', unsafe_allow_html=True)
        
        # Input messaggio
        with st.form("chat_form", clear_on_submit=True):
            new_msg = st.text_input("Scrivi un messaggio...")
            if st.form_submit_button("Invia 🚀") and new_msg:
                now = datetime.now().strftime("%H:%M")
                messages.append({"user": name, "time": now, "text": new_msg})
                save_data("chat.json", messages)
                st.rerun()

else:
    st.title("🏯 ACCEDI AL PORTALE")
    st.image("https://imgur.com", use_container_width=True)
    st.warning("Esegui il login nella barra laterale per chattare e vedere le news.")
