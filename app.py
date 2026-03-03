import streamlit as st
import pickle
import pandas as pd
import requests
import time
import numpy as np
# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="AI Movie Recommender",
    layout="wide"
)

# ==============================
# SAFE REQUEST HANDLER (CRITICAL)
# ==============================
def safe_get(url, params=None, retries=3, timeout=8):
    for _ in range(retries):
        try:
            r = requests.get(url, params=params, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException:
            time.sleep(1)
    return None

# ==============================
# SESSION STATE
# ==============================
if "selected_from_trending" not in st.session_state:
    st.session_state.selected_from_trending = None

# ==============================
# DARK THEME
# ==============================
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #141414;
    color: #ffffff;
    font-family: 'Helvetica Neue', sans-serif;
}
.stButton button {
    background-color: #E50914;
    color: white;
    border-radius: 6px;
    font-weight: 600;
    border: none;
}
.stButton button:hover { background-color: #f40612; }
.movie-card img {
    border-radius: 14px;
    transition: transform 0.3s ease;
}
.movie-card img:hover { transform: scale(1.07); }
.title-text { font-weight: 600; margin-top: 6px; }
.reason-text { font-size: 12px; color: #b3b3b3; }
</style>
""", unsafe_allow_html=True)

# ==============================
# TMDB CONFIG
# ==============================
API_KEY = "8ecced159527d160b4c46b318771664b"
BASE_POSTER_URL = "https://image.tmdb.org/t/p/w500"
PLACEHOLDER = "https://via.placeholder.com/300x450?text=No+Poster"
TMDB_FALLBACK = "https://image.tmdb.org/t/p/w500/8UlWHLMpgZm9bx6QYh0NFoq67TZ.jpg"

def get_poster(poster_path, backdrop_path=None):
    # 1️⃣ Valid poster
    if isinstance(poster_path, str) and poster_path.strip():
        return f"{BASE_POSTER_URL}{poster_path}"

    # 2️⃣ Valid backdrop
    if isinstance(backdrop_path, str) and backdrop_path.strip():
        return f"{BASE_POSTER_URL}{backdrop_path}"

    # 3️⃣ TMDB generic movie image
    return TMDB_FALLBACK

# ==============================
# TMDB API FUNCTIONS
# ==============================
@st.cache_data(ttl=3600)
def fetch_trending_movies():
    data = safe_get(
        "https://api.themoviedb.org/3/trending/movie/day",
        {"api_key": API_KEY}
    )
    return data.get("results", [])[:6] if data else []

@st.cache_data(ttl=3600)
def fetch_movie_details(movie_id):
    data = safe_get(
        f"https://api.themoviedb.org/3/movie/{movie_id}",
        {"api_key": API_KEY, "language": "en-US"}
    )
    if not data:
        return {
            "poster_path": None,
            "backdrop_path": None,
            "genres": [],
            "popularity": 0,
            "release_date": "2000-01-01"
        }
    return data

@st.cache_data(ttl=3600)
def fetch_trailer(movie_id):
    data = safe_get(
        f"https://api.themoviedb.org/3/movie/{movie_id}/videos",
        {"api_key": API_KEY}
    )
    if not data:
        return None
    for v in data.get("results", []):
        if v.get("type") == "Trailer" and v.get("site") == "YouTube":
            return f"https://www.youtube.com/embed/{v['key']}"
    return None

# ==============================
# LOAD DATA
# ==============================
movies = pd.DataFrame(pickle.load(open("movies_dict.pkl", "rb")))
similarity = np.array(pickle.load(open("similarity.pkl", "rb")))

# ==============================
# HEADER
# ==============================
st.markdown("<h1 style='text-align:center;'>🎬 AI Movie Recommender</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#b3b3b3;'>Fast • Accurate • Netflix-style</p>", unsafe_allow_html=True)
st.divider()

# ==============================
# TRENDING MOVIES
# ==============================
st.subheader("🔥 Trending Now")
cols = st.columns(6)
for col, movie in zip(cols, fetch_trending_movies()):
    with col:
        st.image(get_poster(movie.get("poster_path"), movie.get("backdrop_path")), width=130,use_container_width=False)
        if st.button(movie["title"], key=f"trend_{movie['id']}"):
            st.session_state.selected_from_trending = movie["title"]
            st.rerun()

# ==============================
# MOVIE SELECT
# ==============================
default_idx = 0
if st.session_state.selected_from_trending in movies["title"].values:
    default_idx = movies[movies["title"] == st.session_state.selected_from_trending].index[0]

selected_movie = st.selectbox(
    "🎥 Choose a movie you like",
    movies["title"].values,
    index=default_idx
)

# ==============================
# FAST RECOMMENDER (TOP-K ONLY)
# ==============================
def recommend(movie_title, top_n=5):
    idx = movies[movies["title"] == movie_title].index[0]

    scores = similarity[idx]

    # ⚡ FAST partial sort (no full sorting)
    top_idx = np.argpartition(scores, -top_n-1)[-top_n-1:]
    top_idx = top_idx[top_idx != idx]
    top_idx = top_idx[np.argsort(scores[top_idx])[::-1]][:top_n]

    results = []

    for i in top_idx:
        movie_id = movies.iloc[i].movie_id
        details = fetch_movie_details(movie_id)  # ONLY 5 CALLS NOW

        results.append({
            "id": movie_id,
            "title": movies.iloc[i].title,
            "poster": get_poster(
                details.get("poster_path"),
                details.get("backdrop_path")
            ),
            "reason": f"Similarity Score: {round(scores[i]*100,2)}%"
        })

    return results

# ==============================
# RECOMMEND BUTTON
# ==============================
if st.button("✨ Recommend Movies", use_container_width=True):
    with st.spinner("Finding perfect movies for you 🍿"):
        recs = recommend(selected_movie)

    st.subheader("🎯 Recommended For You")
    cols = st.columns(5)
    for col, m in zip(cols, recs):
        with col:
            st.markdown(f"""
            <div class="movie-card">
                <img src="{m['poster']}" width="100%">
                <div class="title-text">{m['title']}</div>
                <div class="reason-text">{m['reason']}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("▶ Trailer", key=f"tr_{m['id']}"):
                t = fetch_trailer(m["id"])
                if t:
                    st.markdown(f"<iframe width='100%' height='250' src='{t}'></iframe>", unsafe_allow_html=True)

# ==============================
# FOOTER
# ==============================
st.markdown(
    "<hr><p style='text-align:center;color:#777;'>Built with Streamlit • ML • TMDB API</p>",
    unsafe_allow_html=True
)