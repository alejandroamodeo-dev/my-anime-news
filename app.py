import streamlit as st
import requests
import streamlit_authenticator as stauth

# --- 1. CONFIGURAZIONE E STILE RE:ZERO (Viola & Bianco) ---
st.set_page_config(page_title="Re:Zero Database", page_icon="🦋", layout="wide")

st.markdown("""
    <style>
    /* SFONDO TEMATICO RE:ZERO */
    .stApp {
        background-image: url("https://imgur.com"); /* Sfondo Foresta di Ghiaccio/Emilia */
        background-size: cover;
        background-attachment: fixed;
    }

    /* TRASPARENZA PER FAR VEDERE LO SFONDO */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMainViewContainer"] {
        background-color: rgba(0, 0, 0, 0) !important;
    }

    /* VELO VIOLA SCURO PER LEGGIBILITÀ */
    .main .block-container {
        background-color: rgba(30, 0, 50, 0.8);
        border-radius: 20px;
        padding: 40px;
        border: 2px solid #a020f0;
    }
    
    /* LOGO SIDEBAR */
    .logo-text {
        font-size: 38px !important;
        font-weight: 900;
        color: #a020f0 !important;
        text-align: center;
        text-shadow: 2px 2px 10px #fff;
    }

    /* CARD PERSONAGGI/NEWS */
    .anime-card {
        background-color: white;
        border-radius: 15px;
        padding: 15px;
        color: #000 !important;
        border: 2px solid #a020f0;
    }
    
    h1, h2, h3 { color: #ffffff !important; text-shadow: 2px 2px 5px #a020f0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SISTEMA ACCOUNT ---
if 'users' not in st.session_state:
    st.session_state['users'] = {"usernames": {"admin": {"name": "Subaru", "password": "123", "email": "lugnica@news.it"}}}

authenticator = stauth.Authenticate(st.session_state['users'], "rezero_key", "sig", cookie_expiry_days=30)

st.sidebar.markdown('<p class="logo-text">🦋<br>RE:ZERO INFO</p>', unsafe_allow_html=True)
authenticator.login(location='sidebar')

auth_status = st.session_state.get('authentication_status')

# --- 3. LOGICA VISUALIZZAZIONE ---
if auth_status:
    st.sidebar.success(f"Benvenuto, {st.session_state.get('name')}")
    authenticator.logout('Logout', 'sidebar')
    
    st.title("❄️ RE:ZERO KNOWLEDGE BASE")
    
    # Sezione Info Personaggi o News specifiche
    tab1, tab2 = st.tabs(["📚 PERSONAGGI", "📰 ULTIME NEWS"])
    
    with tab1:
        st.subheader("Personaggi Principali")
        # Qui facciamo una ricerca specifica per Re:Zero nell'API
        try:
            res = requests.get("https://jikan.moe").json().get('data', [])[:6]
            cols = st.columns(3)
            for i, item in enumerate(res):
                char = item['character']
                with cols[i % 3]:
                    st.markdown(f"""
                        <div class="anime-card">
                            <img src="{char['images']['jpg']['image_url']}" style="width:100%; height:250px; object-fit:cover; border-radius:10px;">
                            <h4 style="color:black; margin-top:10px;">{char['name']}</h4>
                            <p style="color:purple;">Ruolo: {item['role']}</p>
                        </div>
                    """, unsafe_allow_html=True)
        except:
            st.error("Errore nel caricamento dei personaggi.")

    with tab2:
        st.subheader("Novità sulla serie")
        st.info("La Stagione 3 è attualmente in produzione/trasmissione! Resta sintonizzato.")

else:
    # SCHERMATA DI BENVENUTO (La tua immagine con i personaggi)
    st.title("🏯 ACCEDI AL PORTALE DI LUGNICA")
    st.image("https://ibb.co", use_container_width=True)
    
    with st.sidebar.expander("🆕 REGISTRATI"):
        try:
            if authenticator.register_user(location='sidebar'):
                st.success('Registrato con successo!')
        except Exception as e:
            st.error(f"Errore: {e}")
