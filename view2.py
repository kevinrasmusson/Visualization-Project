import pandas as pd
from bokeh.plotting import figure, show
from bokeh.layouts import row
from bokeh.models import ColumnDataSource, HoverTool

def hidden_gems(imdb, rotten_tomatoes):
    print("Hidden Gems in movies:")

    # Clean and normalize titles
    imdb['movie_title'] = imdb['movie_title'].str.strip().str.lower()
    rotten_tomatoes['title'] = rotten_tomatoes['title'].str.strip().str.lower()

    # Convert years to same type
    imdb['title_year'] = imdb['title_year'].astype(int)
    rotten_tomatoes['release_date'] = rotten_tomatoes['release_date'].astype(int)

    # Merge datasets on matching columns
    merged = pd.merge(
        imdb,
        rotten_tomatoes,
        left_on=['movie_title', 'title_year'],
        right_on=['title', 'release_date'],
        how='inner'
    )

    # Create new dataset with movie_title and title_year
    result = merged[['movie_title', 'title_year']].copy()

    result['imdb_score'] = merged['imdb_score']
    # Clean audience_score: remove '%' and convert to float
    result['audience_score'] = merged['audience_score'].str.replace('%', '').astype(float) / 10

    # Calculate mean score
    result['mean_score'] = (merged['imdb_score'] + result['audience_score']) / 2

    # Remove duplicates, keeping the first occurrence
    result = result.drop_duplicates(subset=['movie_title', 'title_year'], keep='first')

    print(f"Found {len(result)} matching movies")
    print(result.head())
    print(result.shape)

    return result
