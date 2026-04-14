import streamlit as st
import requests
import streamlit_authenticator as stauth
import time

# --- 1. DESIGN "ULTRA TITAN" ---
st.set_page_config(page_title="My Anime News - Pro", page_icon="🏮", layout="wide")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    .stApp { background: #050508; color: #f0f0f0; font-family: 'Rajdhani', sans-serif; }
    .sakura-container { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 99999; }
    .petal { position: absolute; background-color: #ffb7c5; border-radius: 150% 0 150% 0; opacity: 0.8; filter: drop-shadow(0 0 15px #ffb7c5); animation: fall linear infinite; }
    @keyframes fall { 0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; } 100% { transform: translateY(110vh) rotate(720deg); opacity: 0; } }
    .anime-logo { font-family: 'Bangers', cursive; font-size: clamp(8rem, 25vw, 15rem); text-align: center; color: #fff; text-shadow: 0 0 25px #ff4b4b, 0 0 50px #ff4b4b; margin-top: -140px; line-height: 0.8; position: relative; z-index: 10; }
    .fresche-title { text-align: center; font-size: clamp(1rem, 3vw, 1.8rem); color: #ffffff !important; font-weight: 700; letter-spacing: 12px; margin-top: -10px; margin-bottom: 60px; text-transform: uppercase; display: block; position: relative; z-index: 10; opacity: 0.9; }
    .fresh-card { background: rgba(45, 45, 50, 0.9); border: 2px solid rgba(255, 75, 75, 0.4); border-radius: 15px; padding: 20px; backdrop-filter: blur(10px); height: 500px; }
    </style>
    <div class="sakura-container">
        <div class="petal" style="width:60px; height:60px; left:10%; animation-duration:10s;"></div>
        <div class="petal" style="width:90px; height:90px; left:30%; animation-duration:15s;"></div>
        <div class="petal" style="width:110px; height:110px; left:75%; animation-duration:12s;"></div>
    </div>
""", unsafe_allow_html=True)

# --- 2. ACCOUNT ---
if 'config' not in st.session_state:
    st.session_state.config = {"credentials": {"usernames": {"admin": {"name": "Capo", "password": "$2b$12$K7T6U/f0XpM9kPzN8Ff1.O6R5T7n5.N0v4P0E7S6Z.k6W/F7f5W2K", "email": "a@b.com"}}}, "cookie": {"key": "sakura_v26", "name": "man_cookie_v26", "expiry_days": 30}}

authenticator = stauth.Authenticate(st.session_state.config['credentials'], st.session_state.config['cookie']['name'], st.session_state.config['cookie']['key'], st.session_state.config['cookie']['expiry_days'])
authenticator.login(location='sidebar')
auth_status = st.session_state.get("authentication_status")

# --- 3. MOTORE NEWS (ULTRA-ROBUSTO) ---
@st.cache_data(ttl=3600)
def get_safe_news():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    # Prova Kitsu
    try:
        r = requests.get("https://kitsu.io[status]=current&page[limit]=6", headers=headers, timeout=10)
        if r.status_code == 200:
            return [{'title': a['attributes']['canonicalTitle'], 'img': a['attributes']['posterImage']['large'], 'score': a['attributes']['averageRating']} for a in r.json()['data']]
    except: pass

    # Prova Jikan
    try:
        r = requests.get("https://jikan.moe", headers=headers, timeout=10)
        if r.status_code == 200:
            return [{'title': a['title'], 'img': a['images']['jpg']['large_image_url'], 'score': a.get('score', 'N/D')} for a in r.json()['data'][:6]]
    except: pass

    # DATI DI EMERGENZA (Se tutto fallisce)
    return [
        {'title': 'One Piece', 'img': 'https://kitsu.io', 'score': '90'},
        {'title': 'Naruto Shippuden', 'img': 'https://kitsu.io', 'score': '85'},
        {'title': 'Solo Leveling', 'img': 'https://kitsu.io', 'score': '88'}
    ]

# --- 4. LOGICA ---
if auth_status:
    st.sidebar.write(f"🏮 Shinobi: **{st.session_state.name}**")
    authenticator.logout('Logout', 'sidebar')
    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    st.markdown('<p class="fresche-title">INFORMAZIONI ANIME FRESCHE</p>', unsafe_allow_html=True)

    news = get_safe_news()
    cols = st.columns(3)
    for i, a in enumerate(news):
        with cols[i % 3]:
            st.markdown(f"""<div class="fresh-card">
                <img src="{a['img']}" style="width:100%; height:300px; object-fit:cover; border-radius:10px;">
                <h4 style="color:#ff4b4b; margin-top:10px;">{a['title'][:35]}</h4>
                <p style="color:#ccc;">⭐ Rating: {a['score']}</p>
            </div>""", unsafe_allow_html=True)

elif auth_status is None:
    st.markdown('<p class="anime-logo">MY ANIME NEWS</p>', unsafe_allow_html=True)
    st.markdown('<p class="fresche-title">INFORMAZIONI ANIME FRESCHE</p>', unsafe_allow_html=True)
    with st.sidebar.expander("Non hai un account? Registrati"):
        if authenticator.register_user(location='main'): st.success('Registrato!')
