import pandas as pd
from bokeh.plotting import figure, show
from bokeh.layouts import row
from bokeh.models import ColumnDataSource, HoverTool
def plot_data(imdb_data, rotten_tomatoes_data):
    # Display the first few rows of the datasets
    print("IMDB Data:")
    print(imdb_data.head())
    print("\nRotten Tomatoes Data:")
    print(rotten_tomatoes_data.head())