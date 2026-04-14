import pandas as pd
from bokeh.plotting import figure, show
from bokeh.layouts import row
from bokeh.models import ColumnDataSource, HoverTool
from view1 import plot_data
def main():
    imdb_data = pd.read_csv("imdb_movie_metadata.csv")
    rotten_tomatoes_data = pd.read_csv("movie_info.csv")
    # Remove rows with missing values and duplicates
    imdb_data = imdb_data.dropna()
    rotten_tomatoes_data = rotten_tomatoes_data.dropna()
    imdb_data = imdb_data.drop_duplicates()
    rotten_tomatoes_data = rotten_tomatoes_data.drop_duplicates()

    plot_data(imdb_data, rotten_tomatoes_data)

if __name__ == "__main__":
    main()

#I might do some edits here later