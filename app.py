import streamlit as st
import requests
import streamlit_authenticator as stauth
from datetime import datetime

# --- 1. CONFIGURAZIONE & STILE BRANDIZZATO "MY ANIME NEWS" ---
st.set_page_config(page_title="My Anime News - Portale Ufficiale", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    @import url('https://googleapis.com');

    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 50%, #1a1a2e 0%, #050505 100%);
        color: #e0e0e0;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* LOGO PRINCIPALE MY ANIME NEWS */
    .brand-header {
        font-family: 'Syncopate', sans-serif;
        font-size: 3.5rem;
        text-align: center;
        background: linear-gradient(90deg, #ff4b4b, #ff8080);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        text-shadow: 0 0 25px rgba(255, 75, 75, 0.4);
    }
    
    .brand-subtitle {
        text-align: center;
        letter-spacing: 8px;
        color: #888;
        font-size: 0.9rem;
        margin-bottom: 50px;
        text-transform: uppercase;
    }

    /* NEWS CARD PERSONALIZZATA */
    .news-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-bottom: 20px;
        height: 100%;
        backdrop-filter: blur(12px);
    }

    .news-card:hover {
        background: rgba(255, 255, 255, 0.07);
        border-color: #ff4b4b;
        transform: translateY(-8px);
        box-shadow: 0 15px 45px rgba(255, 75, 75, 0.25);
    }

    .news-tag {
        background: #ff4b4b;
        color: white;
        padding: 5px 15px;
        border-radius: 50px;
        font-size: 0.65rem;
        font-weight: 800;
        text-transform: uppercase;
    }

    .news-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin: 15px 0;
        color: #fff;
        line-height: 1.2;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #0c0c0e !important;
        border-right: 1px solid #222;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SISTEMA ACCOUNT ---
if 'config' not in st.session_state:
    st.session_state['config'] = {
        "credentials": {"usernames": {"admin": {"name": "Redattore MyAnime", "password": "$2b$12$K7T6U/f0XpM9kPzN8Ff1.O6R5T7n5.N0v4P0E7S6Z.k6W/F7f5W2K", "email": "news@myanimenews.it"}}},
        "cookie": {"key": "man_key", "name": "man_cookie", "expiry_days": 30}
    }

authenticator = stauth.Authenticate(
    st.session_state['config']['credentials'],
    st.session_state['config']['cookie']['name'],
    st.session_state['config']['cookie']['key'],
    st.session_state['config']['cookie']['expiry_days']
)

# --- 3. FETCH NEWS ---
@st.cache_data(ttl=300)
def get_live_news():
    try:
        # Recupera i top anime per simulare le news più calde
        r = requests.get("https://jikan.moe")
        return r.json().get('data', [])[:12]
    except:
        return []

# --- 4. LOGICA APP ---
name, auth_status, username = authenticator.login(location='sidebar')

if auth_status:
    # Sidebar Brandizzata
    st.sidebar.markdown("<h2 style='color:#ff4b4b; text-align:center;'>🏮 MAN</h2>", unsafe_allow_html=True)
    st.sidebar.info(f"Redattore: **{name}**")
    authenticator.logout('Chiudi Sessione', 'sidebar')

    # Header Principale
    st.markdown('<h1 class="brand-header">MY ANIME NEWS</h1>', unsafe_allow_html=True)
    st.markdown('<p class="brand-subtitle">Il tuo radar quotidiano sul mondo dell\'animazione</p>', unsafe_allow_html=True)
    
    st.divider()

    news_list = get_live_news()

    if news_list:
        cols = st.columns(3)
        for idx, item in enumerate(news_list):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="news-card">
                        <span class="news-tag">MY ANIME NEWS • ESCLUSIVA</span>
                        <span style="float:right; color:#666; font-size:0.8rem;">{datetime.now().strftime('%H:%M')}</span>
                        <img src="{item['images']['jpg']['large_image_url']}" style="width:100%; height:200px; object-fit:cover; border-radius:12px; margin: 15px 0;">
                        <div class="news-title">{item['title']}</div>
                        <p style="color:#888; font-size:0.9rem;">Ultimi dettagli sulla produzione: lo studio conferma il rilascio di nuovi materiali promozionali.</p>
                    </div>
                """, unsafe_allow_html=True)
                
                with st.expander("LEGGI ARTICOLO COMPLETO"):
                    st.write(f"**Titolo originale:** {item.get('title_japanese', 'N/D')}")
                    st.write("**Report:** La redazione di My Anime News ha analizzato i dati di ascolto e le recensioni critiche. La serie si posiziona tra le più attese della stagione.")
                    st.link_button("FONTE ORIGINALE", item['url'], use_container_width=True)
    else:
        st.warning("📡 Collegamento ai server My Anime News in corso...")

elif auth_status is False:
    st.sidebar.error("Credenziali My Anime News non valide.")
else:
    # Welcome Page "My Anime News"
    st.markdown("""
        <div style="text-align:center; margin-top:100px;">
            <h1 class="brand-header" style="font-size:5rem;">MY ANIME NEWS</h1>
            <p style="font-size:1.4rem; letter-spacing:12px; color:#555;">GATEWAY ACCESSO REDAZIONE</p>
            <div style="background:rgba(255,75,75,0.05); padding:30px; border-radius:20px; border:1px solid rgba(255,75,75,0.3); display:inline-block; margin-top:40px;">
                <p style="margin:0; font-size:1.1rem;">Inserire le credenziali nella barra laterale</p>
                <code style="color:#ff4b4b; background:transparent;">admin | 123</code>
            </div>
        </div>
    """, unsafe_allow_html=True)
