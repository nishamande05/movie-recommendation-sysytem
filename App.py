import streamlit as st
import pickle
import pandas as pd
import requests

import gdown
from os import path

# similarity.pkl download
if not path.exists("similarity.pkl"):
    gdown.download(id="1_0XZ05RTFZLnvW1HHjn3gl9lz6en8q_R", output="similarity.pkl", quiet=False)

# movie_list.pkl download
if not path.exists("movie_list.pkl"):
    gdown.download(id="1HlpVGqR_vfxJa1Oa9kxuaMhc4JwfwPG1", output="movie_list.pkl", quiet=False)
# ------------ CONFIG ------------
OMDB_API_KEY = "9a0e251f"   # <- put your key here
# --------------------------------


# ------------ LOAD DATA ----------
movies = pd.read_pickle('Movies.pkl')

similarity = pd.read_pickle('similarity.pkl')
# ------------ POSTER (OMDb) ----------
# ------------ POSTER (OMDb) ----------
def fetch_poster(title):
    url = "https://www.omdbapi.com/"
    params = {
        "apikey": OMDB_API_KEY,
        "t": title
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        poster_url = data.get("Poster")
        if poster_url and poster_url != "N/A":
            return poster_url
    except Exception:
        return None
    return None

# ------------ RECOMMEND ----------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    movie_index = int(movie_index)
    distances = similarity.values[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster = fetch_poster(movie_id)
        recommended_posters.append(poster)
    return recommended_movies, recommended_posters

# ------------ STREAMLIT UI ----------
st.title("Movie Recommender sysytem")

selected_movie_name = st.selectbox(
    "Select a movie",
    movies["title"].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    for name, poster in zip(names, posters):
        st.subheader(name)
        if poster:
            st.image(poster, width=150)
        else:
            st.write("Poster not available")



