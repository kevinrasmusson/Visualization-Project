from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, HoverTool, RangeSlider, CustomJS, NumeralTickFormatter

def hidden_gems(merged_data):
    """Create Hidden Gems visualization from merged dataset"""
    print(f"Hidden gems found: {len(merged_data)}")

    # Two sources: full data (never mutated) + filtered view (plot reads this)
    full_source = ColumnDataSource(merged_data)
    filtered_source = ColumnDataSource(merged_data)

    # Plot
    plot = figure(
        title="Hidden Gems: High Score, Low Gross",
        x_axis_label="Mean Score (0–10)",
        y_axis_label="Box Office Gross ($)",
        width=850,
        height=550,
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
    )

    plot.yaxis.formatter = NumeralTickFormatter(format="$0,0")

    hover = HoverTool(tooltips=[
        ('Title',  '@movie_title'),
        ('Year',   '@title_year'),
        ('Score',  '@mean_score{0.00}'),
        ('Gross',  '@gross{$0,0}'),
    ])
    plot.add_tools(hover)

    year_min = int(merged_data['title_year'].min())
    year_max = int(merged_data['title_year'].max())
    score_min = float(merged_data['imdb_score'].min())
    score_max = float(merged_data['imdb_score'].max())
    gross_min = float(merged_data['gross'].min())
    gross_max = float(merged_data['gross'].max())

    # Sliders
    year_slider = RangeSlider(
        start=year_min, end=year_max, value=(year_min, year_max),
        step=1, title="Release Year Range", width=850,
    )
    score_slider = RangeSlider(
        start=score_min, end=score_max, value=(score_min, score_max),
        step=0.1, title="IMDB Score Range", width=850,
    )
    gross_slider = RangeSlider(
        start=gross_min, end=gross_max, value=(gross_min, gross_max),
        step=1000000, title="Box Office Gross ($) Range", width=850, format="$0,0"
    )

    # JavaScript callback
    callback = CustomJS(
        args=dict(full=full_source, filtered=filtered_source, year_slider=year_slider,
                  score_slider=score_slider, gross_slider=gross_slider),
        code="""
            const [year_lo, year_hi] = year_slider.value;
            const [score_lo, score_hi] = score_slider.value;
            const [gross_lo, gross_hi] = gross_slider.value;

            const full_data = full.data;
            const new_data = {};
            for (const key of Object.keys(full_data)) {
                new_data[key] = [];
            }

            const years = full_data['title_year'];
            const scores = full_data['imdb_score'];
            const grosses = full_data['gross'];
            for (let i = 0; i < years.length; i++) {
                if (years[i] >= year_lo && years[i] <= year_hi &&
                    scores[i] >= score_lo && scores[i] <= score_hi &&
                    grosses[i] >= gross_lo && grosses[i] <= gross_hi) {
                    for (const key of Object.keys(full_data)) {
                        new_data[key].push(full_data[key][i]);
                    }
                }
            }

            filtered.data = new_data;
        """
    )

    year_slider.js_on_change('value', callback)
    score_slider.js_on_change('value', callback)
    gross_slider.js_on_change('value', callback)

    return column(year_slider, score_slider, gross_slider, plot)