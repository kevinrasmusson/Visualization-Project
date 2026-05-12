from bokeh.plotting import figure
from bokeh.models import HoverTool, NumeralTickFormatter
import pandas as pd

def hidden_gems(filtered_source):
    """Create Hidden Gems visualization from filtered dataset"""
    print(f"Hidden gems plot created for filtered data")

    # Create 4 popularity groups based on num_critic_of_reviews
    data = filtered_source.data
    if 'num_voted_users' in data:
        critic_reviews = data['num_voted_users']
        # Divide into 4 quartiles
        color_map = pd.qcut(critic_reviews, q=4, labels=False, duplicates='drop')
        # Map to 4 distinct colors
        color_palette = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71']  # Red, Orange, Blue, Green
        colors = [color_palette[int(c)] if pd.notna(c) else '#cccccc' for c in color_map]
        filtered_source.data['colors'] = colors

    # Plot
    plot = figure(
        title="Hidden Gems: High Score, Low Gross",
        x_axis_label="Mean Score (0–10)",
        y_axis_label="Box Office Gross ($)",
        width=710,
        height=405,
        tools="pan,wheel_zoom,box_zoom,box_select,lasso_select,reset",
        toolbar_location="above",  # Keep toolbar only on this plot
    )

    plot.scatter(
        x='mean_score',
        y='gross',
        source=filtered_source,
        size=9,
        alpha=0.7,
        color='colors',
        line_color='white',
        line_width=0.5,
        selection_color="red",
        nonselection_alpha=0.1,
    )

    plot.yaxis.formatter = NumeralTickFormatter(format="$0,0")

    hover = HoverTool(tooltips=[
        ('Title',  '@movie_title'),
        ('Year',   '@title_year'),
        ('Score',  '@mean_score{0.00}'),
        ('Gross',  '@gross{$0,0}'),
        ('Genre', '@genres'),
        ('Critic Reviews', '@num_critic_of_reviews'),
    ])
    plot.add_tools(hover)

    return plot