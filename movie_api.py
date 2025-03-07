import requests

API_KEY = "46143507c634a8862ffd3ad5aa5c3868"
BASE_URL = "https://api.themoviedb.org/3"

def get_movie_data(movie_name):
    """Fetch movie details from TMDb API based on a movie name."""
    search_url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={movie_name}"
    response = requests.get(search_url).json()

    if response['results']:
        movie = response['results'][0]  # Get first search result
        return {
            "title": movie['title'],
            "overview": movie['overview'],
            "rating": movie['vote_average'],
            "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
        }
    return None

# Test fetching movie data
if __name__ == "__main__":
    print(get_movie_data("Inception"))
