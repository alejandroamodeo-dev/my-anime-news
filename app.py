
import streamlit as st
import requests
import streamlit_authenticator as stauth

# --- 1. CONFIGURAZIONE E STILE TOTAL DARK + COLORI NEON ---
st.set_page_config(page_title="My Anime News", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    /* Sfondo Nero Assoluto */
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* Sidebar Nero Profondo con bordo Neon */
    [data-testid="stSidebar"] { 
        background-color: #050505; 
        border-right: 1px solid #ff4b4b; 
    }
    
    /* Card Anime con bordi colorati e ombra Neon */
    .anime-card {
        background-color: #0a0a0a;
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #333;
        transition: 0.4s;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.1);
    }
    .anime-card:hover {
        border-color: #00ff41; /* Verde Neon al passaggio */
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
        transform: scale(1.02);
    }
    
    /* Titoli Colorati */
    h1 { color: #ff4b4b !important; text-shadow: 0 0 10px #ff4b4b; font-family: 'Arial Black'; }
    h2, h3, h4 { color: #00d4ff !important; }
    
    /* Bottoni Personalizzati */
    div.stButton > button {
        background-color: #ff4b4b;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        box-shadow: 0 0 10px rgba(255, 75, 75, 0.4);
    }
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

# Sidebar con Logo e Titolo
st.sidebar.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🏮 My Anime News</h1>", unsafe_allow_html=True)
st.sidebar.write("---")

# Gestione Login
authenticator.login(location='sidebar')
auth_status = st.session_state.get('authentication_status')
name = st.session_state.get('name')

# Registrazione
if auth_status is None or auth_status is False:
    with st.sidebar.expander("🆕 CREA ACCOUNT"):
        try:
            if authenticator.register_user(location='sidebar'):
                st.success('Account creato! Accedi sopra.')
        except Exception as e:
            st.error(f"Errore: {e}")

# --- 3. LOGICA DI VISUALIZZAZIONE ---
if auth_status:
    st.sidebar.success(f"ONLINE: {name}")
    authenticator.logout('Logout', 'sidebar')
    
    st.title("🏮 MY ANIME NEWS")
    st.subheader("Database Aggiornato in Tempo Reale")
    st.write("---")

    categoria = st.selectbox("SCEGLI SETTORE:", ["IN CORSO", "PROSSIMAMENTE", "TOP RATED"])

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
        st.warning("⚠️ API in sovraccarico. Ricarica la pagina tra 10 secondi.")
        data = []

    # Griglia a 3 colonne
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
            st.link_button("LEGGI SCHEDA", anime['url'])
            st.write("")

elif auth_status is False:
    st.sidebar.error('Dati errati.')
else:
    # SCHERMATA DI BENVENUTO (Immagine Anime Iniziale)
    st.title("🏮 MY ANIME NEWS")
    st.image("https://alphacoders.com", caption="Benvenuto nel Database Protetto", use_container_width=True)
    st.warning("EFFETTUA IL LOGIN PER CONSULTARE I FILE RISERVATI.")
