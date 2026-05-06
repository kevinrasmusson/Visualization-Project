import pandas as pd
from bokeh.plotting import figure, show
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, HoverTool
from view1 import plot_data
from view2 import hidden_gems
from bokeh.io import output_file

def main():
    imdb_data = pd.read_csv("imdb_movie_metadata.csv")
    rotten_tomatoes_data = pd.read_csv("movie_info.csv")
    # Remove rows with missing values and duplicates
    imdb_data = imdb_data.dropna()

    #Normalizethe format
    rotten_tomatoes_data['release_date'] = pd.to_numeric(rotten_tomatoes_data['release_date'].astype(str).str[-4:],
                                                         errors='coerce').astype('Int64')
    rotten_tomatoes_data = rotten_tomatoes_data.dropna()
    imdb_data = imdb_data.drop_duplicates()
    rotten_tomatoes_data = rotten_tomatoes_data.drop_duplicates()

    # Get plots from both views
    plot1 = plot_data(imdb_data, rotten_tomatoes_data)
    plot2 = hidden_gems(imdb_data, rotten_tomatoes_data)

    # Combine side-by-side
    layout = column(plot2, plot1)

    # Save to HTML
    output_file("combined_views.html")
    show(layout)

if __name__ == "__main__":
    main()
