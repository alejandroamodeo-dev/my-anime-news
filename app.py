
import streamlit as st
import requests
import streamlit_authenticator as stauth

# --- 1. CONFIGURAZIONE PAGINA (Stile Crunchyroll/Bandai) ---
st.set_page_config(page_title="Anime News Portal", page_icon="🧡", layout="wide")

# CSS per colori chiari e arancione vibrante
st.markdown("""
    <style>
    /* Sfondo bianco pulito */
    .stApp { background-color: #FFFFFF; color: #23252b; }
    
    /* Card delle notizie bianche con ombra e bordo arancione al passaggio */
    .anime-card {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: 0.3s;
        margin-bottom: 20px;
    }
    .anime-card:hover {
        border-color: #F47521;
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.1);
    }
    
    /* Titoli in Arancione Crunchyroll */
    h1, h2, h3, h4 { 
        color: #F47521 !important; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
    }
    
    /* Bottoni Arancioni */
    div.stButton > button {
        background-color: #F47521;
        color: white;
        border-radius: 25px;
        border: none;
        width: 100%;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SISTEMA ACCOUNT ---
if 'users' not in st.session_state:
    st.session_state['users'] = {
        "usernames": {
            "admin": {"name": "Admin", "password": "123", "email": "admin@anime.com"}
        }
    }

authenticator = stauth.Authenticate(
    st.session_state['users'], "anime_cookie", "signature_key", cookie_expiry_days=30
)

# Login nella Sidebar
st.sidebar.title("🧡 ACCOUNT LOGIN")
authenticator.login(location='sidebar')

auth_status = st.session_state.get('authentication_status')
name = st.session_state.get('name')

# Registrazione (Mostrata solo se non loggato)
if not auth_status:
    with st.sidebar.expander("Non hai un account? Registrati"):
        try:
            if authenticator.register_user(location='sidebar'):
                st.success('Registrato! Ora puoi entrare.')
        except Exception as e:
            st.error(f"Errore: {e}")

# --- 3. LOGICA DI VISUALIZZAZIONE ---
if auth_status:
    st.sidebar.success(f"Bentornato, {name}!")
    authenticator.logout('Esci dal portale', 'sidebar')
    
    st.title("🏯 Ultime Notizie Anime")
    st.write("Esplora le novità della stagione direttamente dal database Jikan.")

    categoria = st.sidebar.selectbox("SELEZIONA CATEGORIA", ["IN CORSO", "PROSSIMAMENTE", "PIÙ VOTATI"])

    @st.cache_data
    def get_data(mode):
        urls = {
            "IN CORSO": "https://jikan.moe",
            "PROSSIMAMENTE": "https://jikan.moe",
            "PIÙ VOTATI": "https://jikan.moe"
        }
        r = requests.get(urls[mode])
        return r.json().get('data', [])

    data = get_data(categoria)

    # Griglia di notizie
    cols = st.columns(3)
    for i, anime in enumerate(data[:15]):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="anime-card">
                    <img src="{anime['images']['jpg']['large_image_url']}" style="width:100%; border-radius:10px; height:350px; object-fit:cover;">
                    <h4 style="margin-top:15px; font-size:1.1em;">{anime['title'][:35]}...</h4>
                    <p style="color:#666; font-size:0.9em;">⭐ Media Voto: {anime.get('score', 'N/A')}</p>
                </div>
            """, unsafe_allow_html=True)
            st.link_button("LEGGI DI PIÙ", anime['url'])
            st.write("")

elif auth_status is False:
    st.sidebar.error('Credenziali errate.')
    st.title("⚠️ Accesso Negato")
else:
    st.title("🏯 Benvenuto nel Portale Anime")
    st.info("Esegui il login nella barra laterale per consultare le ultime notizie e il database.")
    st.image("https://unsplash.com", caption="Accedi alla community")
