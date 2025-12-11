from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, Range1d


def show_bokeh(suggestions, filename="suggestions.html"):
    """Display suggestions in an interactive Bokeh chart."""
    titles = [s["title"] for s in suggestions]
    scores = [float(s["score"]) for s in suggestions]

    sc_vals = [s.get("rating_sc_global") for s in suggestions]
    sc_strs = [f"{v:.1f}" if isinstance(v, (int, float)) and v is not None else "N/A" for v in sc_vals]

    source = ColumnDataSource(data=dict(
        title=titles,
        score=scores,
        sc_text=sc_strs,
    ))

    p = figure(
        x_range=titles,
        height=500,
        width=1100,
        title="Suggestions (Score IA, SensCritique)"
    )

    p.vbar(x="title", top="score", width=0.8, source=source)

    y_min = min(scores)
    y_max = max(scores)
    margin = max(1, (y_max - y_min) * 0.2)
    p.y_range = Range1d(y_min - margin, y_max + margin)

    p.xaxis.major_label_orientation = 1.2

    p.add_tools(HoverTool(tooltips=[
        ("Titre", "@title"),
        ("Score IA", "@score"),
        ("SC Global", "@sc_text"),
    ]))

    output_file(filename)
    show(p)
