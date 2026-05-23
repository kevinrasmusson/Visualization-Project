import pandas as pd
from bokeh.plotting import show
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Spacer
from view1 import plot_data
from view2 import hidden_gems
from view3 import discovery_heatmap
from view4 import genre_hidden_gems
from bokeh.io import output_file
from controll import create_sliders_and_callback
from bokeh.models import ColumnDataSource, Spacer, Div



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

    merged = pd.merge(
        imdb,
        rt,
        left_on=['movie_title', 'title_year'],
        right_on=['title', 'release_date'],
        how='inner'
    )

    result = merged[['movie_title', 'title_year']].copy()
    result['imdb_score'] = merged['imdb_score']

    result['num_critic_of_reviews'] = merged['num_critic_for_reviews']
    result['num_voted_users'] = merged['num_voted_users']

    result['gross'] = pd.to_numeric(
        merged['gross'].astype(str).str.replace(',', ''),
        errors='coerce'
    )

    result['audience_score'] = (
        merged['audience_score'].str.replace('%', '').astype(float) / 10
    )

    result['mean_score'] = (
        result['imdb_score'] + result['audience_score']
    ) / 2

    result['genres'] = merged['genres']

    result = result.dropna(subset=[
        'gross',
        'mean_score',
        'num_critic_of_reviews',
        'num_voted_users',
        'genres'
    ])

    result = result.drop_duplicates(
        subset=['movie_title', 'title_year'],
        keep='first'
    )

    return result
def add_critic_review_colors(data):
    """Add fixed color groups based on critic review count quartiles."""
    data = data.copy()

    color_palette = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71']

    labels = [
        'Few critic reviews',
        'Some critic reviews',
        'Many critic reviews',
        'Most critic reviews'
    ]

    critic_group = pd.qcut(
        data['num_critic_of_reviews'],
        q=4,
        labels=False,
        duplicates='drop'
    )

    data['colors'] = [
        color_palette[int(group)] if pd.notna(group) else '#cccccc'
        for group in critic_group
    ]

    data['critic_review_group'] = [
        labels[int(group)] if pd.notna(group) else 'Unknown'
        for group in critic_group
    ]

    return data

def main():
    imdb_data = pd.read_csv("imdb_movie_metadata.csv")
    rotten_tomatoes_data = pd.read_csv("movie_info.csv")

    imdb_data = imdb_data.dropna()

    rotten_tomatoes_data['release_date'] = pd.to_numeric(
        rotten_tomatoes_data['release_date'].astype(str).str[-4:],
        errors='coerce'
    ).astype('Int64')

    rotten_tomatoes_data = rotten_tomatoes_data.dropna()
    imdb_data = imdb_data.drop_duplicates()
    rotten_tomatoes_data = rotten_tomatoes_data.drop_duplicates()

    merged_data = prepare_merged_dataset(imdb_data, rotten_tomatoes_data)
    merged_data = add_critic_review_colors(merged_data)

    print(f"Merged dataset size: {len(merged_data)} movies")

    # Full unchanged dataset for callbacks
    source = ColumnDataSource(merged_data)

    # Filtered dataset used by linked plots
    filtered_source = ColumnDataSource(merged_data)

    plot1 = plot_data(filtered_source)

    plot2 = hidden_gems(filtered_source)

    # This heatmap is currently static because it uses the DataFrame directly
    plot3 = discovery_heatmap(merged_data)
    plot4 = genre_hidden_gems(merged_data)
    year_slider, score_slider, gross_slider, genre_select = create_sliders_and_callback(
        merged_data,
        source,
        filtered_source
    )

    header = Div(text="""
    <style>
      .bk-clearfix {
        width: 100% !important;
      }
    </style>
    <div style="
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
        margin-top: -8px;
        width: 100vw;
        font-family: Arial, sans-serif;
        background: #1f2937;
        color: white;
        padding: 18px 24px;
        margin-bottom: 12px;
        text-align: center;
        box-sizing: border-box;
    ">
        <h1 style="margin: 0; font-size: 28px;">Movie Hidden Gems Dashboard</h1>
        <p style="margin: 6px 0 0 0; color: #d1d5db; font-size: 14px;">
            Explore overlooked movies using scores, box office gross, critic-review count, genre, and release decade.
        </p>
        <p style="margin: 6px 0 0 0; color: #d1d5db; font-size: 13px;">
            Use the filters to narrow movies by year, score, gross revenue, and genre. Hover over charts for details.
        </p>
    </div>
    """, sizing_mode="stretch_width")

    filter_title = Div(text="""
    <div style="
        font-family: Arial, sans-serif;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 4px;
    ">
        Filters
    </div>
    """)

    left_controls = column(
        year_slider,
        score_slider,
        width=500
    )

    right_controls = column(
        gross_slider,
        genre_select,
        width=500
    )

    controls = column(
        #filter_title,
        row(Spacer(width=650), filter_title, Spacer(width=650)),
        row(Spacer(width=150), left_controls, Spacer(width=50), right_controls),
        width=1500
    )

    layout = column(
        header,
        controls,
        Spacer(height=20),
        row(plot2, plot1),
        Spacer(height=25),
        row(plot3, plot4),
        sizing_mode="stretch_width"
    )

    output_file("combined_views.html")
    show(layout)


if __name__ == "__main__":
    main()