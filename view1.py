from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool

def plot_data(merged_data):
    """Plot IMDB Score vs Rotten Tomatoes Audience Score from merged dataset"""
    source = ColumnDataSource(data=dict(
        movie_title=merged_data["movie_title"],
        imdb_score=merged_data["imdb_score"],
        rt_audience_score=merged_data["audience_score"],
        rt_audience_percent=merged_data["audience_score"] * 10,
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
        ("RT Audience", "@rt_audience_percent{0.0}%"),
        ("RT Normalized", "@rt_audience_score"),
    ])

    p.add_tools(hover)
    return p