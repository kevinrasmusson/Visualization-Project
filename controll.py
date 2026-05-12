from bokeh.models import RangeSlider, CustomJS, Select


def create_sliders_and_callback(merged_data, full_source, filtered_source):
    """Create sliders, genre selector, and shared callback for filtering both plots"""

    # Extract data ranges for sliders
    year_min = int(merged_data['title_year'].min())
    year_max = int(merged_data['title_year'].max())
    score_min = float(merged_data['imdb_score'].min())
    score_max = float(merged_data['imdb_score'].max())
    gross_min = float(merged_data['gross'].min())
    gross_max = float(merged_data['gross'].max())

    # Create sliders
    year_slider = RangeSlider(
        start=year_min, end=year_max, value=(year_min, year_max),
        step=1, title="Release Year Range", width=550,
    )
    score_slider = RangeSlider(
        start=score_min, end=score_max, value=(score_min, score_max),
        step=0.1, title="Mean Score Range", width=550,
    )
    gross_slider = RangeSlider(
        start=gross_min, end=gross_max, value=(gross_min, gross_max),
        step=1000000, title="Box Office Gross ($) Range", width=550, format="$0,0"
    )

    # Extract unique genres (split by '|' if multiple)
    all_genres = set()
    for genre_str in merged_data['genres'].dropna():
        genres = [g.strip() for g in str(genre_str).split('|')]
        all_genres.update(genres)

    genre_list = sorted(list(all_genres))

    # Create genre selector
    genre_select = Select(
        title="Filter by Genre:",
        value="",  # Empty means "show all"
        options=[("", "")] + [(g, g) for g in genre_list],
        width=550
    )

    # Create shared callback
    callback = CustomJS(
        args=dict(full=full_source, filtered=filtered_source, year_slider=year_slider,
                  score_slider=score_slider, gross_slider=gross_slider, genre_select=genre_select),
        code="""
            const [year_lo, year_hi] = year_slider.value;
            const [score_lo, score_hi] = score_slider.value;
            const [gross_lo, gross_hi] = gross_slider.value;
            const selected_genre = genre_select.value;

            const full_data = full.data;
            const new_data = {};
            for (const key of Object.keys(full_data)) {
                if (key !== 'colors') {
                    new_data[key] = [];
                }
            }

            const years = full_data['title_year'];
            const scores = full_data['mean_score'];
            const grosses = full_data['gross'];
            const genres = full_data['genres'];

            for (let i = 0; i < years.length; i++) {
                // Check basic filters
                const year_match = years[i] >= year_lo && years[i] <= year_hi;
                const score_match = scores[i] >= score_lo && scores[i] <= score_hi;
                const gross_match = grosses[i] >= gross_lo && grosses[i] <= gross_hi;

                // Check genre filter
                let genre_match = true;
                if (selected_genre !== "") {
                    // Split genres by '|' and check if any match
                    const movie_genres = genres[i].split('|').map(g => g.trim());
                    genre_match = movie_genres.includes(selected_genre);
                }

                if (year_match && score_match && gross_match && genre_match) {
                    for (const key of Object.keys(full_data)) {
                        if (key !== 'colors') {
                            new_data[key].push(full_data[key][i]);
                        }
                    }
                }
            }

            // Regenerate colors after filtering
            if ('num_voted_users' in new_data) {
                const color_palette = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71'];
                new_data['colors'] = new_data['num_voted_users'].map(v => color_palette[Math.floor(Math.random() * 4)]);
            }

            filtered.data = new_data;
        """
    )

    # Attach callback to all controls
    year_slider.js_on_change('value', callback)
    score_slider.js_on_change('value', callback)
    gross_slider.js_on_change('value', callback)
    genre_select.js_on_change('value', callback)

    return year_slider, score_slider, gross_slider, genre_select