
import streamlit as st
import requests
import streamlit_authenticator as stauth
import json
import os
from datetime import datetime

# --- 1. CONFIGURAZIONE E FIX VISIVO ---
st.set_page_config(page_title="My Anime News & Chat", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    /* SFONDO MANGA - Link ultra stabile */
    .stApp { 
        background-image: url("https://alphacoders.com"); 
        background-size: cover; 
        background-attachment: fixed; 
    }
    
    /* Rende trasparenti i blocchi neri di sistema */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMainViewContainer"] { 
        background-color: rgba(0, 0, 0, 0) !important; 
    }
    
    /* Contenitore principale semitrasparente per leggere bene */
    .main .block-container { 
        background-color: rgba(0, 0, 0, 0.75); 
        border-radius: 20px; 
        padding: 30px; 
        margin-top: 20px; 
        color: white; 
    }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] { 
        background-color: rgba(0, 0, 0, 0.9) !important; 
        border-right: 2px solid #ff4b4b; 
    }
    
    .logo-text { 
        font-size: 42px !important; 
        font-weight: 900; 
        color: #ff4b4b !important; 
        text-align: center; 
        text-shadow: 3px 3px 10px #000; 
    }

    /* CARD ANIME */
    .anime-card { 
        background-color: white; 
        border-radius: 15px; 
        padding: 15px; 
        color: #000 !important; 
        border: 2px solid #ff4b4b; 
    }
    
    /* BOX CHAT */
    .chat-box { 
        background-color: rgba(255,255,255,0.1); 
        border-radius: 10px; 
        padding: 15px; 
        height: 300px; 
        overflow-y: auto; 
        border: 1px solid #ff4b4b; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTIONE DATI (CHAT) ---
def load_chat():
    if not os.path.exists("chat.json"): return []
    with open("chat.json", "r") as f: return json.load(f)

def save_chat(msgs):
    with open("chat.json", "w") as f: json.dump(msgs, f)

# --- 3. SISTEMA ACCOUNT ---
if 'users' not in st.session_state:
    st.session_state['users'] = {"usernames": {"admin": {"name": "Admin", "password": "123", "email": "a@a.it"}}}

authenticator = stauth.Authenticate(st.session_state['users'], "key", "sig", cookie_expiry_days=30)
st.sidebar.markdown('<p class="logo-text">🏮<br>MY ANIME NEWS</p>', unsafe_allow_html=True)
authenticator.login(location='sidebar')

auth_status = st.session_state.get('authentication_status')

# --- 4. LOGICA SITO ---
if auth_status:
    name = st.session_state.get('name')
    st.sidebar.success(f"Online: {name}")
    authenticator.logout('Logout', 'sidebar')
    
    tab1, tab2 = st.tabs(["📺 NEWS", "💬 CHAT"])

    with tab1:
        st.title("🏮 DATABASE NEWS")
        cat = st.selectbox("CATEGORIA:", ["IN CORSO", "TOP RATED"])
        url = "https://jikan.moe" if cat == "IN CORSO" else "https://jikan.moe"
        
        try:
            res = requests.get(url).json().get('data', [])[:6]
            cols = st.columns(2)
            for i, anime in enumerate(res):
                with cols[i % 2]:
                    st.markdown(f'<div class="anime-card"><img src="{anime["images"]["jpg"]["large_image_url"]}" style="width:100%; height:200px; object-fit:cover;"><h4 style="color:black;">{anime["title"]}</h4></div>', unsafe_allow_html=True)
                    voto = st.slider(f"Voto", 1, 10, 5, key=f"s_{i}")
                    if st.button(f"Vota {i}", key=f"b_{i}"): st.toast("Voto salvato!")
        except: st.error("Errore nel caricamento dati.")

    with tab2:
        st.title("💬 CHAT")
        msgs = load_chat()
        chat_content = "".join([f"<p><b>{m['u']}</b>: {m['t']}</p>" for m in msgs[-15:]])
        st.markdown(f'<div class="chat-box">{chat_content}</div>', unsafe_allow_html=True)
        
        with st.form("msg_form", clear_on_submit=True):
            txt = st.text_input("Messaggio...")
            if st.form_submit_button("Invia") and txt:
                msgs.append({"u": name, "t": txt})
                save_chat(msgs)
                st.rerun()
else:
    st.title("🏯 ACCEDI")
    st.image("https://alphacoders.com", use_container_width=True)
    st.warning("Fai il login a sinistra.")
