from bokeh.plotting import figure
from bokeh.models import HoverTool, NumeralTickFormatter

def hidden_gems(filtered_source):
    """Create Hidden Gems visualization from filtered dataset"""
    print(f"Hidden gems plot created for filtered data")

    # Plot
    plot = figure(
        title="Hidden Gems: High Score, Low Gross",
        x_axis_label="Mean Score (0–10)",
        y_axis_label="Box Office Gross ($)",
        width=850,
        height=550,
        tools="pan,wheel_zoom,box_zoom,box_select,lasso_select,reset",
    )

    plot.scatter(
        x='mean_score',
        y='gross',
        source=filtered_source,
        size=9,
        alpha=0.7,
        color='#2ec4b6',
        line_color='white',
        line_width=0.5,
        selection_color="red",
        nonselection_color='#2ec4b6',
        nonselection_alpha=0.1,
    )

    plot.yaxis.formatter = NumeralTickFormatter(format="$0,0")

    hover = HoverTool(tooltips=[
        ('Title',  '@movie_title'),
        ('Year',   '@title_year'),
        ('Score',  '@mean_score{0.00}'),
        ('Gross',  '@gross{$0,0}'),
        ('Genre', '@genres'),
    ])
    plot.add_tools(hover)

    return plot