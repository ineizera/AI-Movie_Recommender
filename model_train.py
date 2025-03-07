import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load a movie dataset (Download from Kaggle: "TMDb 5000 Movie Dataset")
df = pd.read_csv("movies_1.csv")

# Feature Engineering: Use movie overviews for similarity matching
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(df['overview'].fillna(''))

# Compute cosine similarity between movies
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Save model & TF-IDF vectorizer
joblib.dump((df, tfidf, cosine_sim), "movie_recommender.pkl")
print("Model trained and saved!")
