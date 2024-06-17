import pickle
import streamlit as st
import requests

# Function to fetch the movie poster from TMDB API
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url)
        if response.status_code != 200:
            return None  # Return None if the request failed
        data = response.json()
        poster_path = data.get('poster_path')  # Use get to avoid KeyError
        if not poster_path:
            return None  # Return None if poster_path is missing
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    except Exception as e:
        st.error(f"Error fetching poster: {e}")
        return None

# Function to recommend movies based on the selected movie
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            poster_path = fetch_poster(movie_id)
            if poster_path:  # Append only if a valid poster path is returned
                recommended_movie_posters.append(poster_path)
                recommended_movie_names.append(movies.iloc[i[0]].title)

        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        st.error(f"Error in recommendation process: {e}")
        return [], []

# Load data
try:
    movies = pickle.load(open('movies.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Streamlit UI elements
st.markdown("<h1 style='text-align: center; color: black;'>Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: black;'>Find a similar movie from a dataset of 5,000 movies!</h4>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: black;'>Web App created by Sagar Bapodara</h4>", unsafe_allow_html=True)

# Movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie you like:", movie_list)

# Show recommendations when button is clicked
if st.button('Show Recommendation'):
    st.write("Recommended Movies based on your interests are:")
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    if not recommended_movie_names:
        st.write("No recommendations found.")
    else:
        # Display the recommended movies
        cols = st.columns(5)
        for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
            with col:
                st.text(name)
                st.image(poster)

# Additional spacing to make UI look cleaner
st.title(" ")
