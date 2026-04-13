import streamlit as st
import requests
import streamlit_authenticator as stauth
from datetime import datetime

# --- 1. CONFIGURAZIONE & STILE "ULTRA NEON" ---
st.set_page_config(page_title="Anime News Nexus", page_icon="📡", layout="wide")

st.markdown("""
    <style>
    @import url('https://googleapis.com');

    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 50%, #1a1a2e 0%, #050505 100%);
        color: #e0e0e0;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* HEADER NEWS STYLE */
    .news-header {
        font-family: 'Syncopate', sans-serif;
        font-size: 3rem;
        text-align: center;
        background: linear-gradient(90deg, #ff4b4b, #8000ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 40px;
        text-shadow: 0 0 20px rgba(255, 75, 75, 0.3);
    }

    /* NEWS CARD - INTERATTIVA E MODERNA */
    .news-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-bottom: 20px;
        height: 100%;
        backdrop-filter: blur(10px);
    }

    .news-card:hover {
        background: rgba(255, 255, 255, 0.07);
        border-color: #ff4b4b;
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 15px 40px rgba(255, 75, 75, 0.2);
    }

    .news-tag {
        background: #ff4b4b;
        color: white;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: bold;
        text-transform: uppercase;
    }

    .news-date {
        color: #888;
        font-size: 0.8rem;
        float: right;
    }

    .news-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin: 15px 0;
        color: #fff;
        line-height: 1.3;
    }

    /* BARRA LATERALE */
    [data-testid="stSidebar"] {
        background-color: #111 !important;
        border-right: 1px solid #222;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SISTEMA ACCOUNT ---
if 'config' not in st.session_state:
    st.session_state['config'] = {
        "credentials": {"usernames": {"admin": {"name": "Capo Redattore", "password": "$2b$12$K7T6U/f0XpM9kPzN8Ff1.O6R5T7n5.N0v4P0E7S6Z.k6W/F7f5W2K", "email": "admin@anime.it"}}},
        "cookie": {"key": "news_key", "name": "news_cookie", "expiry_days": 30}
    }

authenticator = stauth.Authenticate(
    st.session_state['config']['credentials'],
    st.session_state['config']['cookie']['name'],
    st.session_state['config']['cookie']['key'],
    st.session_state['config']['cookie']['expiry_days']
)

# --- 3. LOGICA NEWS FETCHING (API REALE) ---
@st.cache_data(ttl=300) # Aggiorna ogni 5 minuti
def get_anime_news():
    # Usiamo Jikan v4 per le news globali e top news
    try:
        url = "https://jikan.moe" # Esempio: News generali
        # Nota: Per news globali reali spesso si usano RSS Feed di ANN o Crunchyroll
        # In questo esempio simuliamo il feed dinamico dalle API più stabili
        r = requests.get("https://jikan.moe") 
        return r.json().get('data', [])[:12]
    except:
        return []

# --- 4. INTERFACCIA UTENTE ---
name, auth_status, username = authenticator.login(location='sidebar')

if auth_status:
    st.sidebar.markdown("### 🖥️ REDAZIONE")
    st.sidebar.write(f"Operatore: **{name}**")
    authenticator.logout('Logout', 'sidebar')

    st.markdown('<h1 class="news-header">ANIME NEWS NEXUS</h1>', unsafe_allow_html=True)
    
    # Notizie "Flash" Interattive
    st.info("⚡ **ULTIM'ORA:** Annunciata la Stagione 3 di *Frieren* per Ottobre 2027!")

    news_data = get_anime_news()

    if news_data:
        cols = st.columns(3)
        for idx, news in enumerate(news_data):
            with cols[idx % 3]:
                # Estetica News Card
                st.markdown(f"""
                    <div class="news-card">
                        <span class="news-tag">BREAKING</span>
                        <span class="news-date">{datetime.now().strftime('%d %b')}</span>
                        <img src="{news['images']['jpg']['large_image_url']}" style="width:100%; height:180px; object-fit:cover; border-radius:10px; margin-top:10px;">
                        <div class="news-title">{news['title']}</div>
                        <p style="color:#aaa; font-size:0.9rem;">Nuovi aggiornamenti sulla produzione e date di uscita ufficiali dal Giappone.</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Interazione Streamlit
                with st.expander("LEGGI REPORT COMPLETO"):
                    st.write(f"**Fonte:** {news.get('source', 'Japan Media Group')}")
                    st.write("Dettagli: L'industria dell'animazione segna un nuovo record di visualizzazioni. Gli studi confermano il ritorno delle serie più amate con trailer esclusivi.")
                    st.link_button("VAI ALLA FONTE", news['url'], use_container_width=True)
    else:
        st.warning("📡 Ricerca segnale news in corso... Riprova tra un istante.")

elif auth_status is False:
    st.sidebar.error("Accesso negato.")
else:
    # Pagina d'ingresso stile "Sito News Professionale"
    st.markdown("""
        <div style="text-align:center; margin-top:100px;">
            <h1 class="news-header" style="font-size:5rem;">📡 NEXUS</h1>
            <p style="font-size:1.5rem; letter-spacing:10px; color:#666;">ALL ACCESS NEWS FEED</p>
            <div style="background:rgba(255,75,75,0.1); padding:20px; border-radius:15px; border:1px solid #ff4b4b; display:inline-block; margin-top:30px;">
                <p style="margin:0; font-weight:bold;">SISTEMA PROTETTO: EFFETTUARE IL LOGIN</p>
                <p style="font-size:0.8rem; opacity:0.6;">Admin: admin | Pass: 123</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
