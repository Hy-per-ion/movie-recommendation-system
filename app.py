import pandas as pd
import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b4dc7323f7d01db24c68c15edf03cd36&language=en-US'.format(movie_id))
    data = response.json()
    poster_path = data['poster_path']
    full_path = 'https://image.tmdb.org/t/p/w500/' + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies_names = []
    recommended_movies_posters = []
    for temp in movies_list:
        movie_id = movies.iloc[temp[0]].movie_id
        recommended_movies_names.append(movies.iloc[temp[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies_names, recommended_movies_posters


movies_dict = pickle.load(open('app/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('app/similarity.pkl', 'rb'))

st.header('Movie Recommender System')
selected_movie_name = st.selectbox('Select Movie:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    num_recommendations = 5
    cols = st.columns(num_recommendations)
    for i in range(num_recommendations):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
