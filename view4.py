import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool


def genre_hidden_gems(merged_data):
    """Bar chart showing average score for low-gross movies by genre."""

    data = merged_data.copy()

    # Focus on lower-gross movies only
    gross_cutoff = data["gross"].quantile(0.50)
    low_gross = data[data["gross"] <= gross_cutoff].copy()

    # Split multi-genre movies into separate rows
    low_gross["genre"] = low_gross["genres"].str.split("|")
    low_gross = low_gross.explode("genre")
    low_gross["genre"] = low_gross["genre"].str.strip()

    grouped = (
        low_gross.groupby("genre")
        .agg(
            avg_score=("mean_score", "mean"),
            movie_count=("movie_title", "count"),
            avg_gross=("gross", "mean"),
        )
        .reset_index()
    )

    # Avoid tiny categories
    grouped = grouped[grouped["movie_count"] >= 5]

    grouped["avg_score"] = grouped["avg_score"].round(2)
    grouped = grouped.sort_values("avg_score", ascending=False).head(12)

    source = ColumnDataSource(grouped)

    p = figure(
        title="Top 12 Genres for Low-Gross, High-Rated Movies",
        x_range=grouped["genre"].tolist(),
        x_axis_label="Genre",
        y_axis_label="Average Mean Score",
        width=620,
        height=390,
        tools="pan,wheel_zoom,box_zoom,reset",
        toolbar_location="above",
    )

    p.vbar(
        x="genre",
        top="avg_score",
        source=source,
        width=0.7,
        alpha=0.8,
    )

    hover = HoverTool(tooltips=[
        ("Genre", "@genre"),
        ("Average score", "@avg_score{0.00}"),
        ("Movies", "@movie_count"),
        ("Average gross", "@avg_gross{$0,0}"),
    ])

    p.add_tools(hover)

    p.xaxis.major_label_orientation = 0.9
    p.y_range.start = 0
    p.grid.grid_line_alpha = 0.25

    return p