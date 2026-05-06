import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, HoverTool, RangeSlider, CustomJS

def hidden_gems(imdb, rotten_tomatoes):
    print("Hidden Gems in movies:")

    # Clean and normalize titles
    imdb['movie_title'] = imdb['movie_title'].str.strip().str.lower()
    rotten_tomatoes['title'] = rotten_tomatoes['title'].str.strip().str.lower()

    # Convert years to same type
    imdb['title_year'] = imdb['title_year'].astype(int)
    rotten_tomatoes['release_date'] = rotten_tomatoes['release_date'].astype(int)

    # Merge datasets
    merged = pd.merge(
        imdb,
        rotten_tomatoes,
        left_on=['movie_title', 'title_year'],
        right_on=['title', 'release_date'],
        how='inner'
    )

    result = merged[['movie_title', 'title_year']].copy()
    result['imdb_score'] = merged['imdb_score']

    # Clean gross
    result['gross'] = pd.to_numeric(
        merged['gross'].astype(str).str.replace(',', ''), errors='coerce'
    )

    # Clean audience_score
    result['audience_score'] = (
        merged['audience_score'].str.replace('%', '').astype(float) / 10
    )

    result['mean_score'] = (result['imdb_score'] + result['audience_score']) / 2
    result = result.dropna(subset=['gross', 'mean_score'])
    result = result.drop_duplicates(subset=['movie_title', 'title_year'], keep='first')

    # Hidden gem filter: high score + low gross
    hidden = result.copy()

    print(f"Hidden gems found: {len(hidden)}")


    # Two sources: full data (never mutated) + filtered view (plot reads this)
    full_source = ColumnDataSource(hidden)
    filtered_source = ColumnDataSource(hidden)  # starts as full, slider updates it

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

    from bokeh.models import NumeralTickFormatter

    # After creating the plot, add this before plot.add_tools(hover):
    plot.yaxis.formatter = NumeralTickFormatter(format="$0,0")

    hover = HoverTool(tooltips=[
        ('Title',  '@movie_title'),
        ('Year',   '@title_year'),
        ('Score',  '@mean_score{0.00}'),
        ('Gross',  '@gross{$0,0}'),
    ])
    plot.add_tools(hover)

    year_min = int(hidden['title_year'].min())
    year_max = int(hidden['title_year'].max())

    score_min = float(hidden['imdb_score'].min())
    score_max = float(hidden['imdb_score'].max())

    gross_min = float(hidden['gross'].min())
    gross_max = float(hidden['gross'].max())

    # Year range slider
    year_slider = RangeSlider(
        start=year_min,
        end=year_max,
        value=(year_min, year_max),
        step=1,
        title="Release Year Range",
        width=850,
    )

    # IMDB score slider
    score_slider = RangeSlider(
        start=score_min,
        end=score_max,
        value=(score_min, score_max),
        step=0.1,
        title="IMDB Score Range",
        width=850,
    )

    gross_slider = RangeSlider(
        start=gross_min,
        end=gross_max,
        value=(gross_min, gross_max),
        step=1000000,  # adjust step size as needed
        title="Box Office Gross ($) Range",
        width=850,
        format="$0,0"
    )

    # JavaScript callback:
    callback = CustomJS(
        args=dict(full=full_source, filtered=filtered_source, year_slider=year_slider, score_slider=score_slider,
                  gross_slider=gross_slider),
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

    output_file("hidden_gems.html")
    show(column(year_slider, score_slider, gross_slider, plot))

    return hidden