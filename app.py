import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import gdown
import os

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Melodify · Music Recommender",
    page_icon="🎵",
    layout="wide",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root variables ── */
:root {
    --bg:        #0a0a0f;
    --surface:   #13131a;
    --card:      #1b1b26;
    --accent:    #e8c547;
    --accent2:   #ff6b6b;
    --text:      #f0eee8;
    --muted:     #7a7a8c;
    --border:    rgba(255,255,255,0.07);
    --radius:    16px;
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}
.stApp { background-color: var(--bg); }

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1300px; margin: auto; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3.5rem 1rem 2.5rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.75rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 900;
    line-height: 1.05;
    margin: 0 0 1rem;
    background: linear-gradient(135deg, var(--text) 40%, var(--accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: var(--muted);
    max-width: 480px;
    margin: 0 auto 2.5rem;
    line-height: 1.7;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border) 30%, var(--border) 70%, transparent);
    margin: 0.5rem 0 2.5rem;
}

/* ── Select box override ── */
div[data-baseweb="select"] > div {
    background-color: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    transition: border-color 0.2s;
}
div[data-baseweb="select"] > div:hover {
    border-color: var(--accent) !important;
}
div[data-baseweb="select"] svg { fill: var(--muted) !important; }

/* ── Button ── */
.stButton > button {
    background: var(--accent) !important;
    color: #0a0a0f !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.65rem 2.2rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 24px rgba(232,197,71,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(232,197,71,0.4) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Label above selector ── */
.selector-label {
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.5rem;
}

/* ── Selector row ── */
.selector-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    max-width: 680px;
    margin: 0 auto 3rem;
}

/* ── Section heading ── */
.section-heading {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 0.3rem;
}
.section-sub {
    font-size: 0.85rem;
    color: var(--muted);
    margin-bottom: 1.8rem;
}

/* ── Music card ── */
.music-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    height: 100%;
}
.music-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 48px rgba(0,0,0,0.5);
    border-color: rgba(232,197,71,0.3);
}
.card-img-wrap {
    position: relative;
    width: 100%;
    aspect-ratio: 1;
    overflow: hidden;
    background: var(--surface);
}
.card-img-wrap img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.4s ease;
}
.music-card:hover .card-img-wrap img { transform: scale(1.06); }
.card-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(10,10,15,0.85) 0%, transparent 55%);
    opacity: 0;
    transition: opacity 0.3s;
    display: flex;
    align-items: flex-end;
    padding: 1rem;
}
.music-card:hover .card-overlay { opacity: 1; }
.play-btn {
    width: 40px; height: 40px;
    background: var(--accent);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    color: #0a0a0f;
    box-shadow: 0 4px 16px rgba(232,197,71,0.4);
}
.card-body {
    padding: 0.9rem 1rem 1rem;
}
.card-rank {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.3rem;
}
.card-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    font-weight: 500;
    color: var(--text);
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* ── Spinner override ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Lazy-load models ────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_data():
    if not os.path.exists('similarity.pkl'):
        with st.spinner("Downloading similarity model…"):
            url = 'https://drive.google.com/uc?id=1Vdf-iWEtphC1g-7ueUDjgj9Xe_mil6iC'
            gdown.download(url, 'similarity.pkl', quiet=False)
    music = pickle.load(open('df.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return music, similarity


@st.cache_resource(show_spinner=False)
def get_spotify_client():
    CLIENT_ID     = "64e80edb421b43a5b1acd767c055c909"
    CLIENT_SECRET = "2cdd2493508c4cdbb90b5082b41a89df"
    ccm = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    return spotipy.Spotify(client_credentials_manager=ccm)


# ── Helpers ─────────────────────────────────────────────────────────────────────
def get_album_cover(sp, song_name: str, artist_name: str) -> str:
    results = sp.search(q=f"track:{song_name} artist:{artist_name}", type="track")
    if results and results["tracks"]["items"]:
        return results["tracks"]["items"][0]["album"]["images"][0]["url"]
    return "https://i.postimg.cc/0QNxYz4V/social.png"


def recommend(music, similarity, sp, song: str):
    idx = music[music['song'] == song].index[0]
    distances = sorted(enumerate(similarity[idx]), key=lambda x: x[1], reverse=True)
    names, posters = [], []
    for i, _ in distances[1:6]:
        row = music.iloc[i]
        posters.append(get_album_cover(sp, row['song'], row['artist']))
        names.append(row['song'])
    return names, posters


# ── UI ──────────────────────────────────────────────────────────────────────────

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ AI-Powered Discovery ✦</div>
    <h1 class="hero-title">Find Your Next<br>Favourite Song</h1>
    <p class="hero-sub">Pick a track you love and let our model surface five songs that match your taste.</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# Load data
music, similarity = load_data()
sp = get_spotify_client()
music_list = music['song'].values

# Selector + button
col_sel, col_btn = st.columns([4, 1], gap="medium")
with col_sel:
    st.markdown('<p class="selector-label">Choose a song</p>', unsafe_allow_html=True)
    selected_song = st.selectbox(
        label="",
        options=music_list,
        label_visibility="collapsed",
    )
with col_btn:
    st.markdown('<p class="selector-label">&nbsp;</p>', unsafe_allow_html=True)
    go = st.button("Discover ✦")

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Recommendations
if go:
    with st.spinner("Finding your next obsession…"):
        names, posters = recommend(music, similarity, sp, selected_song)

    st.markdown(f"""
    <div class="section-heading">Because you liked <em>{selected_song}</em></div>
    <div class="section-sub">5 hand-picked recommendations just for you</div>
    """, unsafe_allow_html=True)

    cols = st.columns(5, gap="large")
    ordinals = ["01", "02", "03", "04", "05"]
    for col, name, poster, rank in zip(cols, names, posters, ordinals):
        with col:
            st.markdown(f"""
            <div class="music-card">
                <div class="card-img-wrap">
                    <img src="{poster}" alt="{name}" />
                    <div class="card-overlay">
                        <div class="play-btn">▶</div>
                    </div>
                </div>
                <div class="card-body">
                    <div class="card-rank">#{rank}</div>
                    <div class="card-title">{name}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)