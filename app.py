import pickle
import streamlit as st
import requests

# Set page configuration
st.set_page_config(
    page_title="CineMate - Movie Recommendations",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
    }
    .title {
        color: #e50914;
        font-size: 3.5rem;
        text-align: center;
        padding: 2rem 0;
        text-shadow: 2px 2px 4px rgba(229, 9, 20, 0.3);
        font-weight: bold;
    }
    .movie-title {
        color: #ffffff;
        font-size: 1.1rem;
        text-align: center;
        padding: 0.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        min-height: 3.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .stButton>button {
        width: 100%;
        background-color: #ffffff;
        color: #000000;
        padding: 0.8rem 1rem;
        border: 2px solid #e50914;
        border-radius: 5px;
        transition: all 0.3s ease;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background-color: #e50914;
        color: #ffffff;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(229, 9, 20, 0.4);
    }
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(229, 9, 20, 0.2);
        border-radius: 5px;
        color: white !important;
    }
    .stSelectbox > div > div:hover {
        border: 1px solid #e50914;
    }
    .movie-card {
        background: rgba(0, 0, 0, 0.7);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(229, 9, 20, 0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    .movie-card:hover {
        transform: translateY(-5px);
        border-color: #e50914;
        box-shadow: 0 4px 20px rgba(229, 9, 20, 0.3);
    }
    img {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
    }
    .stSpinner > div {
        border-top-color: #e50914 !important;
    }
</style>
""", unsafe_allow_html=True)

def fetch_poster(movie_id):
    api_key = "29ad6a51724de2c06c2cc506c5038855"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        with st.spinner('🎬 Fetching movie poster...'):
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get("poster_path")
            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
        return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Main title with custom styling
st.markdown('<h1 class="title">🎬 CineMate</h1>', unsafe_allow_html=True)

# Load data
movies = pickle.load(open('Movie_list.pkl','rb'))
similarity = pickle.load(open('Model.pkl','rb'))
movie_list = movies['title'].values

# Create two columns for layout
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_movie = st.selectbox(
        "🔍 Search for a movie",
        movie_list
    )
    
    if st.button('🎯 Show Recommendations'):
        with st.spinner('🎬 Finding perfect movies for you...'):
            recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
            
            # Create columns for movie recommendations
            cols = st.columns(5)
            for idx, (col, name, poster) in enumerate(zip(cols, recommended_movie_names, recommended_movie_posters)):
                with col:
                    st.markdown(f'<div class="movie-card">', unsafe_allow_html=True)
                    st.markdown(f'<p class="movie-title">{name}</p>', unsafe_allow_html=True)
                    if poster:
                        st.image(poster, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align: center; color: white; padding: 2rem;'>
    Made with ❤️ by CineMate Team
</div>
""", unsafe_allow_html=True)