from flask import Flask, render_template, request, session, redirect, url_for
from movie_api import get_movie_data
import joblib
import numpy as np

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for session management

# Load trained model
df, tfidf, cosine_sim = joblib.load("movie_recommender.pkl")

def get_movie_recommendations(title, num_recs=5):
    if title not in df['title'].values:
        return []
    
    idx = df[df['title'] == title].index[0]
    similarity_scores = list(enumerate(cosine_sim[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:num_recs+1]

    recommended_movies = [df.iloc[i]['title'] for i, _ in similarity_scores]
    return recommended_movies

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = []
    movie_data = None
    error_message = None

    if request.method == "POST":
        movie_name = request.form["movie_name"]
        movie_data = get_movie_data(movie_name)

        if not movie_data:
            error_message = f"Sorry, no results found for '{movie_name}'. Please try another movie."
        else:
            recommendations = get_movie_recommendations(movie_name)

    return render_template("index.html", recommendations=recommendations, movie_data=movie_data, error_message=error_message)

@app.route("/add_favorite", methods=["POST"])
def add_favorite():
    """Add a movie to the favorites list."""
    movie_title = request.form.get("movie_title")

    if "favorites" not in session:
        session["favorites"] = []  # Initialize favorites list

    if movie_title and movie_title not in session["favorites"]:
        session["favorites"].append(movie_title)
        session.modified = True  # Save changes

    return redirect(url_for("index"))

@app.route("/favorites")
def favorites():
    """Display the user's favorite movies."""
    return render_template("favorites.html", favorites=session.get("favorites", []))

@app.route("/clear_favorites")
def clear_favorites():
    """Clear all saved favorites."""
    session.pop("favorites", None)
    return redirect(url_for("favorites"))

@app.route("/movie/<movie_title>")
def movie_details(movie_title):
    """Fetch and display details for a selected movie."""
    movie_data = get_movie_data(movie_title)  # Fetch movie details using API

    if not movie_data:
        return render_template("movie_details.html", error_message=f"Movie '{movie_title}' not found!")

    return render_template("movie_details.html", movie_data=movie_data)


if __name__ == "__main__":
    app.run(debug=True)
