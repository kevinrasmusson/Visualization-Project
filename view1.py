from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool


def plot_data(imdb_data, rotten_tomatoes_data):
    imdb = imdb_data.copy()
    rt = rotten_tomatoes_data.copy()

    # Clean titles for matching
    imdb["title_clean"] = imdb["movie_title"].astype(str).str.strip().str.lower()
    rt["title_clean"] = rt["title"].astype(str).str.strip().str.lower()

    # Convert Rotten Tomatoes audience score from "75%" to 75.0
    rt["audience_score_percent"] = (
        rt["audience_score"]
        .astype(str)
        .str.replace("%", "", regex=False)
    )

    rt["audience_score_percent"] = rt["audience_score_percent"].astype(float)

    # Normalize RT audience score from 0–100 to 0–10
    rt["audience_score_normalized"] = rt["audience_score_percent"] / 10

    # Merge datasets by movie title
    merged = imdb.merge(rt, on="title_clean", how="inner")

    source = ColumnDataSource(data=dict(
        movie_title=merged["movie_title"],
        imdb_score=merged["imdb_score"],
        rt_audience_score=merged["audience_score_normalized"],
        rt_audience_percent=merged["audience_score_percent"],
    ))

    p = figure(
        title="IMDB Score vs Rotten Tomatoes Audience Score",
        x_axis_label="IMDB Score, 0–10",
        y_axis_label="Rotten Tomatoes Audience Score, normalized to 0–10",
        tools="pan,wheel_zoom,box_zoom,reset",
        width=800,
        height=500,
    )

    p.scatter(
        x="imdb_score",
        y="rt_audience_score",
        source=source,
        size=10,
        color="navy",
        alpha=0.5,
    )

    hover = HoverTool(tooltips=[
        ("Movie", "@movie_title"),
        ("IMDB Score", "@imdb_score"),
        ("RT Audience", "@rt_audience_percent%"),
        ("RT Normalized", "@rt_audience_score"),
    ])

    p.add_tools(hover)

    show(p)