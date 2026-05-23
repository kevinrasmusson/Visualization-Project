from bokeh.plotting import figure
from bokeh.models import HoverTool, NumeralTickFormatter, CDSView, GroupFilter
import pandas as pd
def hidden_gems(filtered_source):
    """Create Hidden Gems visualization from filtered dataset"""
    print(f"Hidden gems plot created for filtered data")

    # Create 4 popularity groups based on num_critic_of_reviews


    # Plot
    plot = figure(
        title="Hidden Gems: High Score, Low Gross",
        x_axis_label="Mean Score (0–10)",
        y_axis_label="Box Office Gross ($)",
        width=620,
        height=390,
        tools="pan,wheel_zoom,box_zoom,box_select,lasso_select,reset",
        toolbar_location="above",  # Keep toolbar only on this plot
    )

    critic_groups = [
        ("Few critic reviews", "#e74c3c"),
        ("Some critic reviews", "#f39c12"),
        ("Many critic reviews", "#3498db"),
        ("Most critic reviews", "#2ecc71"),
    ]

    for group_name, group_color in critic_groups:
        view = CDSView(
            filter=GroupFilter(column_name="critic_review_group", group=group_name)
        )

        plot.scatter(
            x='mean_score',
            y='gross',
            source=filtered_source,
            view=view,
            size=9,
            alpha=0.7,
            color=group_color,
            line_color='white',
            line_width=0.5,
            selection_color="red",
            nonselection_alpha=0.1,
            legend_label=group_name,
        )
    plot.legend.title = "Number of Critic Reviews"
    plot.legend.location = "top_left"
    plot.legend.click_policy = "hide"

    plot.yaxis.formatter = NumeralTickFormatter(format="$0,0")

    hover = HoverTool(tooltips=[
        ('Title', '@movie_title'),
        ('Year', '@title_year'),
        ('Score', '@mean_score{0.00}'),
        ('Gross', '@gross{$0,0}'),
        ('Genre', '@genres'),
        ('Number of Critic Reviews', '@num_critic_of_reviews{0,0}'),
        ('Review Count Group', '@critic_review_group'),
    ])
    plot.add_tools(hover)

    return plot