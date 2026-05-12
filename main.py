import pandas as pd
from bokeh.plotting import show
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Spacer
from view1 import plot_data
from view2 import hidden_gems
from bokeh.io import output_file
from controll import create_sliders_and_callback


def prepare_merged_dataset(imdb_data, rotten_tomatoes_data):
    """Merge and clean IMDB and Rotten Tomatoes data - main dataset for all views"""
    imdb = imdb_data.copy()
    rt = rotten_tomatoes_data.copy()

    # Clean and normalize titles
    imdb['movie_title'] = imdb['movie_title'].str.strip().str.lower()
    rt['title'] = rt['title'].str.strip().str.lower()

    # Convert years to same type
    imdb['title_year'] = imdb['title_year'].astype(int)
    rt['release_date'] = rt['release_date'].astype(int)

    # Merge datasets
    merged = pd.merge(
        imdb,
        rt,
        left_on=['movie_title', 'title_year'],
        right_on=['title', 'release_date'],
        how='inner'
    )

    # Extract relevant columns
    result = merged[['movie_title', 'title_year']].copy()
    result['imdb_score'] = merged['imdb_score']

    # Extract relevant columns
    result = merged[['movie_title', 'title_year']].copy()
    result['imdb_score'] = merged['imdb_score']

    # ADD THESE TWO LINES:
    result['num_critic_of_reviews'] = merged[
        'num_critic_for_reviews']  # or 'num_critic_of_reviews' if that's the exact column name
    result['num_voted_users'] = merged['num_voted_users']

    # Clean gross
    result['gross'] = pd.to_numeric(
        merged['gross'].astype(str).str.replace(',', ''), errors='coerce'
    )

    # Clean audience_score
    result['audience_score'] = (
            merged['audience_score'].str.replace('%', '').astype(float) / 10
    )

    result['mean_score'] = (result['imdb_score'] + result['audience_score']) / 2
    result['genres'] = merged['genres']
    result = result.dropna(subset=['gross', 'mean_score'])
    result = result.drop_duplicates(subset=['movie_title', 'title_year'], keep='first')

    return result


def main():
    imdb_data = pd.read_csv("imdb_movie_metadata.csv")
    rotten_tomatoes_data = pd.read_csv("movie_info.csv")

    # Remove rows with missing values and duplicates
    imdb_data = imdb_data.dropna()
    rotten_tomatoes_data['release_date'] = pd.to_numeric(rotten_tomatoes_data['release_date'].astype(str).str[-4:],
                                                         errors='coerce').astype('Int64')
    rotten_tomatoes_data = rotten_tomatoes_data.dropna()
    imdb_data = imdb_data.drop_duplicates()
    rotten_tomatoes_data = rotten_tomatoes_data.drop_duplicates()

    # Create main dataset once
    merged_data = prepare_merged_dataset(imdb_data, rotten_tomatoes_data)
    print(f"Merged dataset size: {len(merged_data)} movies")

    # Create full and filtered sources (shared by both plots)
    full_source = ColumnDataSource(merged_data)
    filtered_source = ColumnDataSource(merged_data)

    # In the main() function, update:
    year_slider, score_slider, gross_slider, genre_select = create_sliders_and_callback(
        merged_data, full_source, filtered_source
    )

    # Pass filtered_source to both plots
    plot1 = plot_data(filtered_source)
    plot2 = hidden_gems(filtered_source)

    # Create 2x2 grid layout for controls with padding
    spacer_h = Spacer(width=250)  # Adjust width value as needed (in pixels)
    controls_row1 = row(year_slider, spacer_h, score_slider)
    controls_row2 = row(gross_slider, spacer_h, genre_select)
    controls_grid = column(controls_row1, controls_row2)
    view_lay = row(plot1, plot2)
    # Combine grid with plots below
    layout = column(controls_grid, view_lay)

    # Save to HTML
    output_file("combined_views.html")
    show(layout)


if __name__ == "__main__":
    main()