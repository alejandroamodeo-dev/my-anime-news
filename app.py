import streamlit as st
import requests
import streamlit_authenticator as stauth

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="My Anime News Pro", page_icon="🏮", layout="wide")

# --- 2. STILE CSS (GRIGIO ANTRACITE + EFFETTI VETRO) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #1e2124;
        background-image: radial-gradient(at 0% 0%, rgba(255,75,75,0.1) 0px, transparent 50%);
    }
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 40px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .logo-text {
        font-size: 38px !important;
        font-weight: 900;
        color: #ff4b4b !important;
        text-align: center;
        line-height: 1.2;
    }
    .anime-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: 0.3s;
        height: 440px;
        margin-bottom: 10px;
    }
    .anime-card:hover {
        border-color: #ff4b4b;
        transform: translateY(-5px);
    }
    h1, h2, h3 { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SISTEMA ACCOUNT (FIX KEYERROR) ---
# Password '123' hashata per compatibilità con stauth
hashed_passwords = ['$2b$12$K7T6U/f0XpM9kPzN8Ff1.O6R5T7n5.N0v4P0E7S6Z.k6W/F7f5W2K'] 

if 'config' not in st.session_state:
    st.session_state['config'] = {
        "credentials": {
            "usernames": {
                "admin": {
                    "name": "Admin",
                    "password": hashed_passwords[0],
                    "email": "admin@anime.it"
                }
            }
        },
        "cookie": {"expiry_days": 30, "key": "anime_signature_key", "name": "anime_auth_cookie"},
        "pre-authorized": {"emails": []}
    }

authenticator = stauth.Authenticate(
    st.session_state['config']['credentials'],
    st.session_state['config']['cookie']['name'],
    st.session_state['config']['cookie']['key'],
    st.session_state['config']['cookie']['expiry_days']
)

# --- 4. LOGIN & LOGICA ---
st.sidebar.markdown('<p class="logo-text">🏮<br>MY ANIME NEWS</p>', unsafe_allow_html=True)
authenticator.login(location='sidebar')

# Recupero stati sessione
auth_status = st.session_state.get('authentication_status')
name = st.session_state.get('name')

if auth_status:
    st.sidebar.success(f"Online: {name}")
    authenticator.logout('Logout', 'sidebar')
    
    st.title("🏮 NOTIZIE RECENTI")
    categoria = st.selectbox("FILTRA PER:", ["IN CORSO", "PROSSIMAMENTE", "I PIÙ VOTATI"])
    
    # Mappatura corretta API Jikan v4
    url_map = {
        "IN CORSO": "https://jikan.moe",
        "PROSSIMAMENTE": "https://jikan.moe",
        "I PIÙ VOTATI": "https://jikan.moe"
    }

    try:
        with st.spinner("Caricamento database..."):
            r = requests.get(url_map[categoria])
            data = r.json().get('data', [])[:12] if r.status_code == 200 else []
            
        if data:
            cols = st.columns(3)
            for i, anime in enumerate(data):
                with cols[i % 3]:
                    st.markdown(f"""
                        <div class="anime-card">
                            <img src="{anime['images']['jpg']['large_image_url']}" style="width:100%; height:280px; object-fit:cover; border-radius:10px;">
                            <h4 style="color:#ff4b4b; margin-top:10px; font-size:1.1rem;">{anime['title'][:35]}...</h4>
                            <p style="font-size:0.8rem; color:#aaa;">Punteggio: {anime.get('score', 'N/A')}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.link_button("APRI SCHEDA", anime['url'], use_container_width=True)
        else:
            st.warning("⚠️ Database momentaneamente occupato (troppe richieste). Riprova tra un istante.")
    except Exception as e:
        st.error(f"Errore di connessione: {e}")

elif auth_status is False:
    st.sidebar.error("Username o Password errati.")
elif auth_status is None:
    # Pagina di Benvenuto per utenti non loggati
    st.markdown("""
        <div style="background: rgba(255, 75, 75, 0.05); padding: 60px; border-radius: 20px; text-align: center; border: 1px solid #ff4b4b;">
            <h1 style="color: #ff4b4b !important; font-size: 3rem;">🏯 BENVENUTO NEL DATABASE</h1>
            <p style="color: white; font-size: 1.2rem;">Accedi dalla barra laterale per consultare le ultime novità del mondo Anime.</p>
            <p style="color: #666; font-size: 0.9rem;">User: admin | Pass: 123</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar.expander("🆕 REGISTRATI"):
        try:
            if authenticator.register_user(location='main'):
                st.success('Registrato con successo! Ora puoi fare il login.')
        except Exception as e:
            st.error(f"Errore registrazione: {e}")
