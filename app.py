import streamlit as st
import requests
import streamlit_authenticator as stauth
import json
from datetime import datetime

# --- 1. DESIGN "ULTRA TITAN" ---
st.set_page_config(page_title="My Anime News - AniList Edition", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    .stApp { background: #050508; color: #f0f0f0; font-family: 'Rajdhani', sans-serif; }

    .sakura-container { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 99999; }
    .petal { position: absolute; background-color: #ffb7c5; border-radius: 150% 0 150% 0; opacity: 0.8; filter: drop-shadow(0 0 15px #ffb7c5); animation: fall linear infinite; }
    @keyframes fall { 0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; } 100% { transform: translateY(110vh) rotate(720deg); opacity: 0; } }

    .anime-logo { 
        font-family: 'Bangers', cursive; 
        font-size: clamp(8rem, 25vw, 18rem); 
        text-align: center; color: #fff; 
        text-shadow: 0 0 25px #ff4b4b, 0 0 50px #ff4b4b, 0 0 100px #ff4b4b; 
        margin-top: -160px; line-height: 0.8; position: relative; z-index: 10; white-space: nowrap;
    }

    .fresche-title { 
        text-align: center; font-size: clamp(1rem, 3vw, 1.8rem); color: #ffffff !important; 
        font-weight: 700; letter-spacing: 12px; margin-top: -20px; margin-bottom: 70px; 
        text-transform: uppercase; display: block; position: relative; z-index: 10; opacity: 0.9;
    }

    .fresh-card { 
        background: rgba(45, 45, 50, 0.9); border: 2px solid rgba(255, 75, 75, 0.4); 
        border-radius: 15px; padding: 25px; backdrop-filter: blur(10px); height: 550px; 
    }
    </style>

    <div class="sakura-container">
        <div class="petal" style="width:70px; height:70px; left:5%; animation-duration:7s;"></div>
        <div class="petal" style="width:100px; height:100px; left:25%; animation-duration:12s;"></div>
        <div class="petal" style="width:120px; height:120px; left:75%; animation-duration:15s;"></div>
    </div>
""", unsafe_allow_html=True)

# --- 2. SISTEMA ACCOUNT ---
if 'config' not in st.session_state:
    st.session_state.config = {
        "credentials": {"usernames": {"admin": {"name": "Redattore Capo", "password": "$2b$12$K7T6U/f0XpM9kPzN8Ff1.O6R5T7n5.N0v4P0E7S6Z.k6W/F7f5W2K", "email": "admin@myanimenews.it"}}},
        "cookie": {"key": "sakura_v20_anilist", "name": "man_cookie_v20", "expiry_days": 30}
    }

authenticator = stauth.Authenticate(st.session_state.config['credentials'], st.session_state.config['cookie']['name'], st.session_state.config['cookie']['key'], st.session_state.config['cookie']['expiry_days'])
authenticator.login(location='sidebar')
auth_status = st.session_state.get("authentication_status")
name = st.session_state.get("name")

# --- 3. FUNZIONI API ANILIST (NUOVE E STABILI) ---
def fetch_anilist(query, variables):
    url = 'https://anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables})
    return response.json()

@st.cache_data(ttl=3600)
def get_seasonal_anime():
    query = '''
    query ($season: MediaSeason, $seasonYear: Int) {
      Page(perPage: 9) {
        media(season: $season, seasonYear: $seasonYear, type: ANIME, sort: POPULARITY_DESC) {
          title { romaji }
          coverImage { large }
          averageScore
          description
          siteUrl
        }
      }
    }
    '''
    # Calcolo stagione attuale
    month = datetime.now().month
    year = datetime.now().year
    season = "SPRING" if 3 <= month <= 5 else "SUMMER" if 6 <= month <= 8 else "FALL" if 9 <= month <= 11 else "WINTER"
    
    variables = {'season': season, 'seasonYear': year}
    data = fetch_anilist(query, variables)
    return data['data']['Page']['media']

def search_anilist(search_text):
    query = '''
    query ($search: String) {
      Page(perPage: 6) {
        media(search: $search, type: ANIME, sort: POPULARITY_DESC) {
          title { romaji }
          coverImage { large }
          averageScore
          siteUrl
        }
      }
    }
    '''
    variables = {'search': search_text}
    data = fetch_anilist(query, variables)
    return data['data']['Page']['media']

# --- 4. LOGICA VISUALIZZAZIONE ---
if auth_status:
    st.sidebar.write(f"🏮 Shinobi: **{name}**")
    menu = st.sidebar.radio("SISTEMA", ["🏠 News", "🔍 Cerca Anime", "💬 Chat"])
    authenticator.logout('Logout', 'sidebar')

    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    st.markdown('<p class="fresche-title">INFORMAZIONI ANIME FRESCHE</p>', unsafe_allow_html=True)

    if menu == "🏠 News":
        news = get_seasonal_anime()
        cols = st.columns(3)
        for i, a in enumerate(news):
            with cols[i % 3]:
                st.markdown(f"""<div class="fresh-card">
                    <img src="{a['coverImage']['large']}" style="width:100%; height:280px; object-fit:cover; border-radius:10px;">
                    <h4 style="color:#ff4b4b; margin-top:10px;">{a['title']['romaji'][:40]}</h4>
                    <p style="color:#ccc;">⭐ Score: {a['averageScore'] if a['averageScore'] else '??'}</p>
                </div>""", unsafe_allow_html=True)
                with st.expander("Trama"):
                    st.write(a['description'].replace('<br>', '')[:200] if a['description'] else "Nessuna descrizione.")
                    st.link_button("Vai alla fonte", a['siteUrl'])

    elif menu == "🔍 Cerca Anime":
        st.subheader("🔍 Ricerca Istantanea")
        query = st.text_input("Cerca un titolo...")
        if query:
            results = search_anilist(query)
            cols = st.columns(3)
            for i, a in enumerate(results):
                with cols[i % 3]:
                    st.markdown(f"""<div class="fresh-card">
                        <img src="{a['coverImage']['large']}" style="width:100%; height:280px; object-fit:cover; border-radius:10px;">
                        <h4 style="color:#ff4b4b; margin-top:10px;">{a['title']['romaji']}</h4>
                        <p style="color:#ccc;">⭐ Score: {a['averageScore'] if a['averageScore'] else '??'}</p>
                    </div>""", unsafe_allow_html=True)
                    st.link_button("Apri Scheda", a['siteUrl'])

elif auth_status is None:
    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    st.markdown('<p class="fresche-title">INFORMAZIONI ANIME FRESCHE</p>', unsafe_allow_html=True)
    with st.sidebar.expander("Non hai un account? Registrati"):
        if authenticator.register_user(location='main'):
            st.success('Registrato! Accedi ora.')
    st.markdown("<div style='text-align:center;'><h3>ACCEDI DALLA SIDEBAR PER CONTINUARE</h3></div>", unsafe_allow_html=True)
