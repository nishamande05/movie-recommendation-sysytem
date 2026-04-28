import streamlit as st
import pickle
import pandas as pd
import requests
from os import path

OMDB_API_KEY = "9a0e251f"

# LOAD DATA
movies = pd.read_pickle('Movies.pkl')
similarity = pickle.load(open('movie_list.pkl', 'rb'))

# Download movie_list.pkl (similarity matrix)
if not path.exists("movie_list.pkl"):
    gdown.download(id="1HlpVGqR_vfxJa1Oa9kxuaMhc4JwfwPG1", output="movie_list.pkl", quiet=False)

OMDB_API_KEY = "9a0e251f"

# LOAD DATA
movies = pd.read_pickle('Movies.pkl')
similarity = pickle.load(open('movie_list.pkl', 'rb'))

# POSTER
def fetch_poster(title):
    url = "https://www.omdbapi.com/"
    params = {"apikey": OMDB_API_KEY, "t": title}
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        poster_url = data.get("Poster")
        if poster_url and poster_url != "N/A":
            return poster_url
    except Exception:
        return None
    return None

# RECOMMEND
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    movie_index = int(movie_index)

    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: float(x[1]))[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))
    return recommended_movies, recommended_posters

# STREAMLIT UI
st.title("Movie Recommender System")

selected_movie_name = st.selectbox("Select a movie", movies["title"].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for idx, (name, poster) in enumerate(zip(names, posters)):
        with cols[idx]:
            st.text(name)
            if poster:
              st.image(poster, width=200)
            else:
                st.write("No poster")

