import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie details using OMDB API
def fetch_movie_details(movie_id):
    url = f"http://www.omdbapi.com/?t={movie_id}&apikey=fb92d22b"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        poster = data.get('Poster', "https://via.placeholder.com/300x450.png?text=No+Image")
        description = data.get('Plot', 'No description available.')
        cast = data.get('Actors', 'No cast available.')
        rating = data.get('imdbRating', 'No rating')
        genre = data.get('Genre', 'No genre')
        release_date = data.get('Released', 'No release date')
        runtime = data.get('Runtime', 'No runtime available')

        return poster, description, cast, rating, genre, release_date, runtime

    return (
        "https://via.placeholder.com/300x450.png?text=No+Image",
        'No description available.',
        'No cast available.',
        'No rating',
        'No genre',
        'No release date',
        'No runtime available'
    )

# Function to recommend movies based on similarity
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_descriptions = []
    recommended_movies_casts = []
    recommended_movies_ratings = []
    recommended_movies_genres = []
    recommended_movies_release_dates = []
    recommended_movies_runtimes = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]]['title']
        poster, description, cast, rating, genre, release_date, runtime = fetch_movie_details(movie_id)

        recommended_movies.append(movies.iloc[i[0]]['title'])
        recommended_movies_posters.append(poster)
        recommended_movies_descriptions.append(description)
        recommended_movies_casts.append(cast)
        recommended_movies_ratings.append(rating)
        recommended_movies_genres.append(genre)
        recommended_movies_release_dates.append(release_date)
        recommended_movies_runtimes.append(runtime)

    return (
        recommended_movies,
        recommended_movies_posters,
        recommended_movies_descriptions,
        recommended_movies_casts,
        recommended_movies_ratings,
        recommended_movies_genres,
        recommended_movies_release_dates,
        recommended_movies_runtimes
    )

# Load movies and similarity data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI for the recommender system
st.set_page_config(page_title='Movie Recommender System', layout='wide')
st.title('🎬 Movie Recommender System')
st.markdown("<h2 style='text-align: center; color: blue;'>Find your next favorite movie!</h2>", unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    'Type or select a movie to get recommendations',
    movies['title'].values)

if st.button('Recommend'):
    with st.spinner('Fetching recommendations...'):
        try:
            (
                names,
                posters,
                descriptions,
                casts,
                ratings,
                genres,
                release_dates,
                runtimes
            ) = recommend(selected_movie_name)

            cols = st.columns(5)
            for idx, col in enumerate(cols):
                with col:
                    st.image(posters[idx], use_container_width=True)  # ✅ Fixed deprecation warning
                    st.markdown(f"**{names[idx]}**")
                    st.markdown(f"⭐ IMDb Rating: {ratings[idx]}")
                    st.markdown(f"🎭 Genre: {genres[idx]}")
                    st.markdown(f"📅 Release Date: {release_dates[idx]}")
                    st.markdown(f"⏳ Runtime: {runtimes[idx]}")
                    st.text(descriptions[idx])
                    st.text(f"🎭 Cast: {casts[idx]}")
        except IndexError:
            st.error("Error fetching recommendations. Please check your data.")

# Adding footer
st.markdown("<hr>", unsafe_allow_html=True)
