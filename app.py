
import streamlit as st
import requests
import streamlit_authenticator as stauth

# --- 1. CONFIGURAZIONE E STILE MANGA VISIBILE ---
st.set_page_config(page_title="My Anime News", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    /* SFONDO MANGA BEN VISIBILE */
    .stApp {
        background-image: url("https://wallpaperaccess.com");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }

    /* Rende il contenuto leggibile ma lascia vedere lo sfondo */
    .main {
        background-color: rgba(0, 0, 0, 0.4); /* Molto più trasparente */
    }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] { 
        background-color: rgba(0, 0, 0, 0.8) !important; 
        border-right: 2px solid #ff4b4b; 
    }
    
    /* LOGO GIGANTE */
    .logo-text {
        font-size: 45px !important;
        font-weight: 900;
        color: #ff4b4b !important;
        text-align: center;
        text-shadow: 2px 2px 10px #000;
        margin-bottom: 30px;
    }

    /* CARD ANIME */
    .anime-card {
        background-color: rgba(255, 255, 255, 0.9); /* Card bianche per contrasto con sfondo manga */
        border-radius: 15px;
        padding: 15px;
        color: #000;
        border: 2px solid #ff4b4b;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
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

    cols = st.columns(3)
    for i, anime in enumerate(data[:12]):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="anime-card">
                    <img src="{anime['images']['jpg']['large_image_url']}" style="width:100%; border-radius:10px; height:300px; object-fit:cover;">
                    <h4 style="color:#000; margin-top:10px;">{anime['title'][:30]}</h4>
                </div>
            """, unsafe_allow_html=True)
            st.link_button("DETTAGLI", anime['url'])

else:
    # IMMAGINE ANIME INIZIALE (Grande e chiara)
    st.title("🏯 ACCEDI AL PORTALE")
    st.image("https://alphacoders.com", use_container_width=True)
    st.warning("Esegui il login nella barra laterale per vedere i contenuti.
