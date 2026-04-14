import pandas as pd
from bokeh.plotting import figure, show
from bokeh.layouts import row
from bokeh.models import ColumnDataSource, HoverTool
def main():
    imdb_data = pd.read_csv("imdb_movie_metadata.csv")
    rotten_tomatoes_data = pd.read_csv("movie_info.csv")

if __name__ == "__main__":
    main()