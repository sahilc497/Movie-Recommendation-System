import streamlit as st
import pandas as pd
import pickle
import requests

# =====================
# CONFIG
# =====================
TMDB_API_KEY = "8e588448dfde9740d31ed82400cf8f27"
PLACEHOLDER_POSTER = "https://via.placeholder.com/500x750?text=No+Poster"

# =====================
# FUNCTIONS
# =====================
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
        else:
            return PLACEHOLDER_POSTER

    except requests.exceptions.RequestException:
        # Handles timeout, connection error, API error
        return PLACEHOLDER_POSTER


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommend_movies = []
    recommend_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))

    return recommend_movies, recommend_movies_posters


# =====================
# LOAD DATA
# =====================
movie_list = pickle.load(open("movie_list.pkl", "rb"))
movies = pd.DataFrame(movie_list)

similarity = pickle.load(open("similarity.pkl", "rb"))

# =====================
# UI
# =====================
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System")

selected_movie_name = st.selectbox(
    "Select a movie",
    movies["title"].values
)

if st.button("Recommend"):
    with st.spinner("Finding similar movies..."):
        names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.subheader(names[i])
            st.image(posters[i], use_column_width=True)

st.markdown("---")
st.caption("Created by **Sahil Chavan**")
