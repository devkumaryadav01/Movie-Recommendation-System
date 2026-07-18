# Import Libraries
import pandas as pd

# Load datasets
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

# Display first 5 rows
#print("Movies Dataset:")
#print(movies.head())

#print("\nRatings Dataset:")
#print(ratings.head())
#print("\nNumber of Movies:", movies.shape)
#print("Number of Ratings:", ratings.shape)

#print("\nMovies Columns:")
#print(movies.columns)

#print("\nRatings Columns:")
#print(ratings.columns)
# Merge both datasets
data = pd.merge(ratings, movies, on="movieId")

#print("\nMerged Dataset:")
#print(data.head())

#print("\nMerged Dataset Shape:")
#print(data.shape)
# Count ratings for each movie
movie_ratings = data.groupby("title")["rating"].count().reset_index()

movie_ratings.rename(columns={"rating": "num_of_ratings"}, inplace=True)

#print("\nMovie Ratings Count:")
#print(movie_ratings.head())
# Create pivot table
movie_matrix = data.pivot_table(
    index="userId",
    columns="title",
    values="rating"
)

#print("\nMovie Matrix:")
#print(movie_matrix.head())
# Choose a movie
movie_name = "Toy Story (1995)"

# Find similarity
similar_movies = movie_matrix.corrwith(movie_matrix[movie_name])

similar_movies = similar_movies.dropna()

#print("\nTop 10 Similar Movies:")
#print(similar_movies.sort_values(ascending=False).head(10))
# Average rating and number of ratings
ratings_stats = data.groupby("title")["rating"].agg(["mean", "count"])
ratings_stats.rename(columns={"mean": "avg_rating", "count": "num_ratings"}, inplace=True)

# Similarity DataFrame
corr_df = similar_movies.to_frame(name="correlation")
corr_df = corr_df.join(ratings_stats)

# Keep movies with at least 100 ratings
recommendations = corr_df[corr_df["num_ratings"] >= 100].sort_values(
    "correlation", ascending=False
)

#print("\nTop Recommended Movies:")
#print(recommendations.head(10))
movie_name = input("Enter movie name: ")

if movie_name not in movie_matrix.columns:
    print("Movie not found! Please enter a valid movie name.")
else:
    similar_movies = movie_matrix.corrwith(movie_matrix[movie_name]).dropna()

    ratings_stats = data.groupby("title")["rating"].agg(["mean", "count"])
    ratings_stats.rename(
        columns={"mean": "avg_rating", "count": "num_ratings"},
        inplace=True
    )

    corr_df = similar_movies.to_frame(name="correlation")
    corr_df = corr_df.join(ratings_stats)

    recommendations = corr_df[corr_df["num_ratings"] >= 100]
    recommendations = recommendations.sort_values(
        "correlation", ascending=False
    )

    print("\nTop 10 Recommended Movies:\n")
    print(recommendations.head(10))
def recommend(movie_name):
    if movie_name not in movie_matrix.columns:
        print("Movie not found! Please enter a valid movie name.")
        return

    similar_movies = movie_matrix.corrwith(movie_matrix[movie_name]).dropna()

    ratings_stats = data.groupby("title")["rating"].agg(["mean", "count"])
    ratings_stats.rename(
        columns={"mean": "avg_rating", "count": "num_ratings"},
        inplace=True
    )

    corr_df = similar_movies.to_frame(name="correlation")
    corr_df = corr_df.join(ratings_stats)

    recommendations = corr_df[corr_df["num_ratings"] >= 100]
    recommendations = recommendations.sort_values(
        "correlation", ascending=False
    )

    print("\nTop 10 Recommended Movies:\n")
    print(recommendations.head(10))


movie = input("Enter movie name: ")
recommend(movie)