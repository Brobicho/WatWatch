from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, Range1d
from bokeh.layouts import column


def show_bokeh(suggestions, filename="suggestions.html"):
    """Display suggestions in an interactive Bokeh chart."""
    # Sort suggestions by AI score (descending) for first chart
    sorted_by_ai = sorted(suggestions, key=lambda x: float(x["score"]), reverse=True)
    
    # Add year to title display for first chart
    titles_ai = []
    for s in sorted_by_ai:
        title = s["title"]
        year = s.get("year")
        if year:
            title = f"{title} ({year})"
        titles_ai.append(title)
    
    scores_ai = [float(s["score"]) for s in sorted_by_ai]
    sc_vals_ai = [s.get("rating_sc_global") for s in sorted_by_ai]
    sc_strs_ai = [f"{v:.1f}" if isinstance(v, (int, float)) and v is not None else "N/A" for v in sc_vals_ai]

    # Sort suggestions by average score (descending) for second chart
    suggestions_with_avg = []
    for s in suggestions:
        score = float(s["score"])
        sc_val = s.get("rating_sc_global")
        if isinstance(sc_val, (int, float)) and sc_val is not None:
            avg = (score + sc_val * 10) / 2
        else:
            avg = score
        suggestions_with_avg.append((s, avg))
    
    suggestions_with_avg.sort(key=lambda x: x[1], reverse=True)
    sorted_by_avg = [s for s, _ in suggestions_with_avg]
    
    # Add year to title display for second chart
    titles_avg = []
    for s in sorted_by_avg:
        title = s["title"]
        year = s.get("year")
        if year:
            title = f"{title} ({year})"
        titles_avg.append(title)
    
    scores_avg = [float(s["score"]) for s in sorted_by_avg]
    sc_vals_avg = [s.get("rating_sc_global") for s in sorted_by_avg]
    sc_strs_avg = [f"{v:.1f}" if isinstance(v, (int, float)) and v is not None else "N/A" for v in sc_vals_avg]

    # Calculate averages for second chart
    averages = []
    avg_strs = []
    for i, sc_val in enumerate(sc_vals_avg):
        if isinstance(sc_val, (int, float)) and sc_val is not None:
            sc_normalized = sc_val * 10
            avg = (scores_avg[i] + sc_normalized) / 2
            averages.append(avg)
            avg_strs.append(f"{avg:.1f}")
        else:
            averages.append(scores_avg[i])
            avg_strs.append("N/A")

    # First chart: AI Scores (sorted by AI score)
    source1 = ColumnDataSource(data=dict(
        title=titles_ai,
        score=scores_ai,
        sc_text=sc_strs_ai,
    ))

    p1 = figure(
        x_range=titles_ai,
        height=500,
        width=1100,
        title="Suggestions (Score IA)"
    )

    p1.vbar(x="title", top="score", width=0.8, source=source1, color="#4285f4")

    y_min = min(scores_ai)
    y_max = max(scores_ai)
    margin = max(1, (y_max - y_min) * 0.2)
    p1.y_range = Range1d(y_min - margin, y_max + margin)

    p1.xaxis.major_label_orientation = 1.2

    p1.add_tools(HoverTool(tooltips=[
        ("Titre", "@title"),
        ("Score IA", "@score"),
        ("SC Global", "@sc_text"),
    ]))

    # Second chart: Average Scores (sorted by average)
    source2 = ColumnDataSource(data=dict(
        title=titles_avg,
        average=averages,
        ai_score=scores_avg,
        sc_text=sc_strs_avg,
        avg_text=avg_strs,
    ))

    p2 = figure(
        x_range=titles_avg,
        height=500,
        width=1100,
        title="Moyenne Score IA et SensCritique"
    )

    p2.vbar(x="title", top="average", width=0.8, source=source2, color="#34a853")

    y_min2 = min(averages)
    y_max2 = max(averages)
    margin2 = max(1, (y_max2 - y_min2) * 0.2)
    p2.y_range = Range1d(y_min2 - margin2, y_max2 + margin2)

    p2.xaxis.major_label_orientation = 1.2

    p2.add_tools(HoverTool(tooltips=[
        ("Titre", "@title"),
        ("Moyenne", "@avg_text"),
        ("Score IA", "@ai_score"),
        ("SC Global", "@sc_text"),
    ]))

    # Combine charts vertically
    layout = column(p1, p2)

    output_file(filename)
    show(layout)
