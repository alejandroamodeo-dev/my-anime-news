
import streamlit as st
import requests
import streamlit_authenticator as stauth

# --- 1. CONFIGURAZIONE E STILE (UGUALE A PRIMA) ---
st.set_page_config(page_title="ANIME NETWORK | DATABASE", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #00ff41; }
    .anime-card {
        background-color: #1a1c23;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #333;
        transition: transform 0.3s;
        margin-bottom: 20px;
    }
    .anime-card:hover { border-color: #00ff41; transform: translateY(-5px); }
    h1, h2, h3 { color: #00ff41 !important; text-shadow: 0 0 10px #00ff41; font-family: 'Courier New'; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SISTEMA ACCOUNT (COMPLESSITÀ AGGIUNTA) ---
if 'users' not in st.session_state:
    st.session_state['users'] = {
        "usernames": {
            "admin": {"name": "Admin", "password": "123", "email": "admin@test.com"}
        }
    }

authenticator = stauth.Authenticate(
    st.session_state['users'], "anime_cookie", "signature_key", cookie_expiry_days=30
)

# Interfaccia Login nella Sidebar
st.sidebar.title("🔑 ACCESS_CONTROL")
# Modifica questa riga: non assegnare variabili qui
authenticator.login(location='sidebar')

# Aggiungi queste righe subito sotto per recuperare i dati correttamente
authentication_status = st.session_state.get('authentication_status')
name = st.session_state.get('name')
username = st.session_state.get('username')

# Pulsante Registrazione nella Sidebar
with st.sidebar.expander("Non hai un account? Registrati"):
    try:
        if authenticator.register_user('Registra Account', preauthorization=False):
            st.success('Utente registrato! Ora puoi accedere.')
    except Exception as e:
        st.error(f"Errore: {e}")

# --- 3. LOGICA DI VISUALIZZAZIONE ---
if authentication_status:
    # Se loggato, mostra il sito di prima
    st.sidebar.success(f"Loggato come: {name}")
    authenticator.logout('Logout', 'sidebar')
    
    st.title("⚡ ANIME_DATABASE_v1.0")
    st.write("---")

    categoria = st.sidebar.selectbox("SELEZIONA_SETTORE", ["TRENDING", "UPCOMING", "TOP_RATED"])

    @st.cache_data
    def get_anime_data(mode):
        endpoints = {
            "TRENDING": "https://jikan.moe",
            "UPCOMING": "https://jikan.moe",
            "TOP_RATED": "https://jikan.moe"
        }
        r = requests.get(endpoints[mode])
        return r.json().get('data', [])

    data = get_anime_data(categoria)

    cols = st.columns(4)
    for i, anime in enumerate(data[:20]):
        with cols[i % 4]:
            st.markdown(f"""
                <div class="anime-card">
                    <img src="{anime['images']['jpg']['large_image_url']}" style="width:100%; border-radius:5px;">
                    <p style="margin-top:10px; font-weight:bold;">{anime['title'][:25]}...</p>
                    <p style="font-size:12px; color:#888;">SCORE: {anime.get('score', '??')}</p>
                </div>
            """, unsafe_allow_html=True)
            st.link_button("OPEN_FILE", anime['url'])

elif authentication_status == False:
    st.error('Username o password errati.')
    st.title("⚠️ ACCESSO NEGATO")
elif authentication_status == None:
    st.title("🛡️ DATABASE PROTETTO")
    st.warning("Effettua il login nella barra laterale per consultare i file.")
