import pandas as pd
from view1 import plot_data


def main():
    imdb_data = pd.read_csv("imdb_movie_metadata.csv")
    rotten_tomatoes_data = pd.read_csv("movie_info.csv")

    # Only keep rows that have the columns needed for this plot
    imdb_data = imdb_data.dropna(subset=["movie_title", "imdb_score"])
    rotten_tomatoes_data = rotten_tomatoes_data.dropna(subset=["title", "audience_score"])

    imdb_data = imdb_data.drop_duplicates()
    rotten_tomatoes_data = rotten_tomatoes_data.drop_duplicates()

    plot_data(imdb_data, rotten_tomatoes_data)


if __name__ == "__main__":
    main()