import pandas as pd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper, ColorBar
from bokeh.palettes import Viridis256


def discovery_heatmap(merged_data):
    """Heatmap for exploring hidden-gem regions by decade and gross category."""

    data = merged_data.copy()

    # decade column
    data["decade"] = (data["title_year"] // 10 * 10).astype(int).astype(str) + "s"

    # gross categories
    data["gross_category"] = pd.qcut(
        data["gross"],
        q=4,
        labels=["Very low gross", "Low gross", "Medium gross", "High gross"]
    )

    # Aggregate data
    grouped = (
        data.groupby(["decade", "gross_category"], observed=True)
        .agg(
            avg_score=("mean_score", "mean"),
            avg_gross=("gross", "mean"),
            movie_count=("movie_title", "count"),
            min_year=("title_year", "min"),
            max_year=("title_year", "max"),
        )
        .reset_index()
    )

    grouped["avg_score"] = grouped["avg_score"].round(2)

    decades = sorted(grouped["decade"].unique())
    gross_categories = ["Very low gross", "Low gross", "Medium gross", "High gross"]

    source = ColumnDataSource(grouped)

    color_mapper = LinearColorMapper(
        palette=Viridis256,
        low=grouped["avg_score"].min(),
        high=grouped["avg_score"].max()
    )

    p = figure(
        title="Hidden Gem Regions: Average Score by Decade and Gross Level",
        x_range=decades,
        y_range=gross_categories,
        width=620,
        height=390,
        x_axis_label="Release decade",
        y_axis_label="Box office gross category",
        tools="pan,wheel_zoom,reset,hover",
    )

    p.rect(
        x="decade",
        y="gross_category",
        width=1,
        height=1,
        source=source,
        fill_color={"field": "avg_score", "transform": color_mapper},
        line_color="white",
        line_width=2,
    )

    hover = HoverTool(tooltips=[
        ("Decade", "@decade"),
        ("Gross category", "@gross_category"),
        ("Average score", "@avg_score"),
        ("Average gross", "@avg_gross{$0,0}"),
        ("Number of movies", "@movie_count"),
        ("Year range", "@min_year - @max_year"),
    ])

    p.add_tools(hover)

    color_bar = ColorBar(
        color_mapper=color_mapper,
        label_standoff=12,
        title="Average score"
    )

    p.add_layout(color_bar, "right")
    p.background_fill_color = "#eeeeee"
    p.xaxis.major_label_orientation = 0.8
    p.ygrid.grid_line_color = None
    p.xgrid.grid_line_color = None

    return p
