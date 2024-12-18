from dash import html, dcc
from datetime import datetime


date_picker = dcc.DatePickerRange(
    id = "date-picker",
    start_date = datetime(2015, 1, 1),
    end_date = datetime.today().date(),
    min_date_allowed = datetime(2015, 1, 1),
    max_date_allowed = datetime.today().date(),
    display_format = 'DD/MM/YYYY',
    style={"width": "120"}
)

color_picker = dcc.Checklist(
    [
        {
            "label": [
                html.Img(
                     src="/assets/color_symbols/white.svg",
                     height=30,
                     width=30,
                     style={"padding-left": 10, "padding-bottom": 10}
                ),
                html.Span("White", style={"font-size": 15, "padding-left": 10, "padding-right": 10}),
            ],
            "value": "W",
        },
        {
            "label": [
                html.Img(
                    src="/assets/color_symbols/blue.svg",
                    height=30,
                    width=30,
                    style={"padding-left": 10, "padding-bottom": 10}
                ),
                html.Span("Blue", style={"font-size": 15, "padding-left": 10, "padding-right": 10}),
            ],
            "value": "U",
        },
        {
            "label": [
                html.Img(
                    src="/assets/color_symbols/black.svg",
                    height=30,
                    width=30,
                    style={"padding-left": 10, "padding-bottom": 10}
                ),
                html.Span("Black", style={"font-size": 15, "padding-left": 10, "padding-right": 10}),
            ],
            "value": "B",
        },
        {
            "label": [
                html.Img(
                    src="/assets/color_symbols/red.svg",
                    height=30,
                    width=30,
                    style={"padding-left": 10, "padding-bottom": 10}
                ),
                html.Span("Red", style={"font-size": 15, "padding-left": 10, "padding-right": 10}),
            ],
            "value": "R",
        },
        {
            "label": [
                html.Img(
                    src="/assets/color_symbols/green.svg",
                    height=30,
                    width=30,
                    style={"padding-left": 10, "padding-bottom": 10}
                ),
                html.Span("Green", style={"font-size": 15, "padding-left": 10, "padding-right": 10}),
            ],
            "value": "G",
        },
    ],
    value=["W", "U", "B", "R", "G"],
    id='color-picker',
    inline=True,
    style={"padding-top": 5}
)

platform_selector = dcc.Checklist(
    id='platform-selector',
    options=[
        {'label': 'Paper', 'value': 'paper'},
        {'label': 'Arena', 'value': 'arena'},
    ],
    value=['paper', 'arena'],
    inputStyle={"margin-right": "5px"},
)

color_filter_style = dcc.Dropdown(
    id='color-filter-style',
    options=[
        {'label': 'At most these colors', 'value': 'at_most'},
        {'label': 'Exactly these colors', 'value': 'exactly'},
        {'label': 'Including these colors', 'value': 'including'},
    ],
    value='at_most',
    searchable=False
)

general_stats = html.Div(
    id='general-stats',
    children='General stats, such as win rate, will be shown here'
)