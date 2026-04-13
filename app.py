
import streamlit as st
import requests
import streamlit_authenticator as stauth

# --- 1. CONFIGURAZIONE E STILE MANGA BACKGROUND ---
st.set_page_config(page_title="My Anime News", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    /* SFONDO MANGA INTERO */
    .stApp {
        background-image: url("https://wallpaperaccess.com");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }

    /* Overlay nero per rendere leggibile il testo sopra lo sfondo manga */
    .stApp > div {
        background-color: rgba(0, 0, 0, 0.85);
    }
    
    /* SIDEBAR SCURA */
    [data-testid="stSidebar"] { 
        background-color: rgba(5, 5, 5, 0.95); 
        border-right: 2px solid #ff4b4b; 
    }
    
    /* LOGO GRANDE NELLA SIDEBAR */
    .logo-text {
        font-size: 45px !important;
        font-weight: 900;
        color: #ff4b4b !important;
        text-align: center;
        text-shadow: 2px 2px 15px rgba(255, 75, 75, 0.7);
        margin-bottom: 30px;
        line-height: 1;
    }

    /* CARD ANIME */
    .anime-card {
        background-color: rgba(20, 20, 20, 0.9);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #444;
        transition: 0.4s;
    }
    .anime-card:hover {
        border-color: #ff4b4b;
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(255, 75, 75, 0.4);
    }
    
    h1, h2, h3 { color: #ff4b4b !important; text-shadow: 0 0 10px #ff4b4b; }
    h4 { color: #00d4ff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SISTEMA ACCOUNT ---
if 'users' not in st.session_state:
    st.session_state['users'] = {
        "usernames": {
            "admin": {"name": "Admin", "password": "123", "email": "admin@anime.it"}
        }
    }

authenticator = stauth.Authenticate(
    st.session_state['users'], "anime_cookie_key", "signature_key", cookie_expiry_days=30
)

# LOGO GIGANTE NELLA SIDEBAR
st.sidebar.markdown('<p class="logo-text">🏮<br>MY ANIME NEWS</p>', unsafe_allow_html=True)
st.sidebar.write("---")

# Gestione Login
authenticator.login(location='sidebar')
auth_status = st.session_state.get('authentication_status')
name = st.session_state.get('name')

# Registrazione
if auth_status is None or auth_status is False:
    with st.sidebar.expander("🆕 REGISTRATI"):
        try:
            if authenticator.register_user(location='sidebar'):
                st.success('Registrato! Accedi sopra.')
        except Exception as e:
            st.error(f"Errore: {e}")

# --- 3. LOGICA DI VISUALIZZAZIONE ---
if auth_status:
    st.sidebar.success(f"ONLINE: {name}")
    authenticator.logout('Logout', 'sidebar')
    
    st.title("🏮 DATABASE AGGIORNATO")
    st.write("---")

    categoria = st.selectbox("FILTRA CATEGORIA:", ["IN CORSO", "PROSSIMAMENTE", "TOP RATED"])

    @st.cache_data(ttl=3600)
    def get_data(mode):
        urls = {
            "IN CORSO": "https://jikan.moe",
            "PROSSIMAMENTE": "https://jikan.moe",
            "TOP RATED": "https://jikan.moe"
        }
        try:
            r = requests.get(urls[mode])
            if r.status_code == 200:
                return r.json().get('data', [])
            return []
        except:
            return []

    data = get_data(categoria)
    if not data:
        data = []

    # Griglia
    cols = st.columns(3)
    for i, anime in enumerate(data[:12]):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="anime-card">
                    <img src="{anime['images']['jpg']['large_image_url']}" style="width:100%; border-radius:10px; height:350px; object-fit:cover;">
                    <h4 style="margin-top:15px;">{anime['title'][:30]}...</h4>
                    <p style="color:#00ff41; font-weight:bold;">Voto: {anime.get('score', '??')}</p>
                </div>
            """, unsafe_allow_html=True)
            st.link_button("APRI SCHEDA", anime['url'])
            st.write("")

elif auth_status is False:
    st.sidebar.error('Username/Password errati.')
else:
    # SCHERMATA BENVENUTO
    st.title("🏮 BENVENUTO NEL PORTALE")
    st.image("https://wallpapercave.com", use_container_width=True)
    st.info("Esegui il login a sinistra per consultare il database manga/anime.")
