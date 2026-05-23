from bokeh.plotting import figure
from bokeh.models import HoverTool

def plot_data(filtered_source):
    """Plot IMDB Score vs Rotten Tomatoes Audience Score from filtered dataset"""
    p = figure(
        title="IMDB Score vs Rotten Tomatoes Audience Score",
        x_axis_label="IMDB Score, 0–10",
        y_axis_label="Rotten Tomatoes Audience Score, normalized to 0–10",
        tools="pan,wheel_zoom,box_zoom,box_select,lasso_select,reset",
        width=620,
        height = 390,
        toolbar_location="above",  # Hide toolbar on this plot
    )

    p.scatter(
        x="imdb_score",
        y="audience_score",
        source=filtered_source,
        size=10,
        color="navy",
        alpha=0.5,
        selection_color="red",
        nonselection_color="navy",
        nonselection_alpha=0.1,
    )

    hover = HoverTool(tooltips=[
        ("Movie", "@movie_title"),
        ("IMDB Score", "@imdb_score"),
        ("RT Audience", "@audience_score{0.00}"),
    ])

    p.add_tools(hover)
    return p