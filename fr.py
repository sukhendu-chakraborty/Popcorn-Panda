import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=e547e17d4e91f3e62a571655cd1ccaff&language=en-US"
    response = requests.get(url)
    data = response.json()
    
    if "poster_path" in data and data["poster_path"] is not None:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i, _ in movies_list:
        movie_id = movies.iloc[i].movie_id
        recommended_movies.append(movies.iloc[i].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


def load_similarity():
    url = "https://github.com/sukhendu-chakraborty/Popcorn-Panda/releases/download/movie/similarity.pkl"
    data = requests.get(url).content
    return pickle.loads(data)
similarity = load_similarity()
movies = pickle.load(open('movies.pkl','rb'))
movie_list = movies['title'].values

st.title('Popcorn Panda 🍿🐼')

selected_movie_name = st.selectbox(
    'Select a movie you like:',
    movie_list
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])



