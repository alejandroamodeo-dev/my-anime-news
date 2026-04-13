
import streamlit as st
import requests
import streamlit_authenticator as stauth

# --- 1. CONFIGURAZIONE E STILE TOTAL DARK ---
st.set_page_config(page_title="Anime Portal Ultra Dark", page_icon="📺", layout="wide")

st.markdown("""
    <style>
    /* Sfondo Nero Assoluto */
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* Sidebar Nero Profondo */
    [data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #1a1a1a; }
    
    /* Card Nero su Nero con bordo sottile */
    .anime-card {
        background-color: #0a0a0a;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #1a1a1a;
        transition: 0.4s;
    }
    .anime-card:hover {
        border-color: #d35400; /* Arancione Bandai scuro */
        background-color: #0f0f0f;
        transform: scale(1.01);
    }
    
    /* Titoli in Arancione Scuro */
    h1, h2, h3, h4 { color: #d35400 !important; font-family: 'Arial Black', sans-serif; }
    
    /* Testi descrittivi grigio cenere */
    p, span, label { color: #aaaaaa !important; }

    /* Bottoni stile Dark Mode */
    div.stButton > button {
        background-color: #d35400;
        color: white;
        border: none;
        border-radius: 4px;
        font-weight: bold;
    }
    
    /* Nasconde elementi bianchi superflui */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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
    st.session_state['users'], "anime_cookie", "signature_key", cookie_expiry_days=30
)

# Login nella Sidebar
st.sidebar.title("🛂 LOGIN_SECURE")
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
    authenticator.logout('Esci', 'sidebar')
    
    st.title("📺 DATABASE NOTIZIE ANIME")
    st.write("---")

    categoria = st.selectbox("FILTRO_SETTORE", ["IN CORSO", "PROSSIMAMENTE", "TOP_RATED"])

    @st.cache_data
    def get_data(mode):
        urls = {
            "IN CORSO": "https://jikan.moe",
            "PROSSIMAMENTE": "https://jikan.moe",
            "TOP_RATED": "https://jikan.moe"
        }
        r = requests.get(urls[mode])
        return r.json().get('data', [])

    data = get_data(categoria)

    cols = st.columns(3)
    for i, anime in enumerate(data[:12]):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="anime-card">
                    <img src="{anime['images']['jpg']['large_image_url']}" style="width:100%; border-radius:5px; height:320px; object-fit:cover; filter: brightness(0.8);">
                    <h4 style="margin-top:10px; font-size:16px;">{anime['title'][:30]}...</h4>
                </div>
            """, unsafe_allow_html=True)
            st.link_button("APRI_FILE", anime['url'])

elif auth_status is False:
    st.sidebar.error('Dati errati.')
else:
    st.title("🏯 ACCESSO PROTETTO")
    st.image("https://wallpapercave.com", use_container_width=True)
    st.warning("Inserisci le credenziali nel terminale a sinistra.")
