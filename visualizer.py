from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import plotly.graph_objects as go
from pandas.core.frame import DataFrame
import enums
import dash_bootstrap_components as dbc
import emoji
from dataframe_calculations import get_event_data, get_multi_dropdown_data, get_statistics, add_score_data, get_general_statistics, filter_colors, add_date_formats, filter_date_range
from enums import ColorNames
from datetime import datetime
from static_design_elements import date_picker, color_picker, general_stats, color_filter_style
import re

#TODO: GITHUB  PAGES
CSV_PATH = 'event_results.csv'

def set_up_initial_figure(dataframe: DataFrame) -> go.Figure:
    initial_figure = go.Figure()
    initial_hover_data = get_event_data(dataframe=dataframe)
    initial_figure.add_trace(
        go.Bar(
            x=df.display_date,
            y=df.wins,
            marker_color='#00CC96',
            name="Wins",
            showlegend=True,
            hovertemplate=initial_hover_data
        )
    )
    initial_figure.add_trace(
        go.Scatter(
            x=df.display_date,
            y=df.max_wins,
            mode='markers',
            marker_color='red',
            name="Max wins",
            showlegend=True,
            marker=dict(size=12, line=dict(width=2, color='Black')),
            opacity=0.8
        )
    )
    initial_figure.update_traces(marker_line_color='#636EFA', marker_line_width=1)
    initial_figure.update_xaxes(autorange="reversed")
    return initial_figure


def set_up_initial_color_pies(dataframe: DataFrame) -> (go.Figure, go.Figure):
    initial_color_pie = go.Figure()
    initial_splash_pie = go.Figure()
    statistics = get_statistics(dataframe=dataframe)
    initial_color_pie.add_trace(
        go.Pie(
            labels=list(statistics["color_statistics"].keys()),
            values=list(statistics["color_statistics"].values()),
            sort=False,
            direction='clockwise',
            marker=dict(
                colors=[color.value for color in enums.ColorsRGBValues]
            )
        )
    )
    initial_splash_pie.add_trace(
        go.Pie(
            labels=list(statistics["splash_statistics"].keys()),
            values=list(statistics["splash_statistics"].values()),
            sort=False,
            direction='clockwise',
            marker=dict(
                colors=[color.value for color in enums.ColorsRGBValues]
            )
        )
    )
    return initial_color_pie, initial_splash_pie


df = pd.read_csv(CSV_PATH)
df = add_score_data(df)
add_date_formats(df)

app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])


initial_fig = set_up_initial_figure(dataframe=df)

initial_color_pie_fig, initial_splash_pie_fig = set_up_initial_color_pies(dataframe=df)

set_names_for_multi_dropdown = get_multi_dropdown_data(dataframe=df)


set_selector = dcc.Dropdown(
    set_names_for_multi_dropdown,
    value=[f'{set_names_for_multi_dropdown[0]["value"]}', f'{set_names_for_multi_dropdown[1]["value"]}'],
    # labelStyle={"display": "flex", "align-items": "center"},
    id='set-selector',
    style={"width": "100%"},
    multi=True,
    placeholder="Select one or more sets",
    maxHeight=250,
)

format_checklist = dcc.Checklist(
    sorted(df.format.unique()),
    value=['Draft'],
    inputStyle={"margin-right": "5px"},
    id='format-selector',
)

event_info_holder = html.Div(
    id='event-info-holder',
    children=[]
)

event_graph = dcc.Graph(
    figure=initial_fig,
    id='events-data',
)

color_pie = dcc.Graph(
    figure=initial_color_pie_fig,
    id='color-statistics'
)

splash_pie = dcc.Graph(
    figure=initial_splash_pie_fig,
    id='splash-statistics'
)

platform_selector = dcc.Checklist(
    id='platform-selector',
    options=[
        {'label': 'Paper', 'value': 'paper'},
        {'label': 'Arena', 'value': 'arena'},
    ],
    value=['paper'],
    inputStyle={"margin-right": "5px"},
)

# App layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [
            dbc.Col(
                [
                    html.H2("MTG Limited Visualizer"),
                ],
                ),
            ],
            align="end"
        ),
        html.Hr(),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                set_selector,
                                html.Br(),
                                dbc.Row(
                                    [
                                        html.Div(
                                            [
                                                format_checklist,
                                                html.Br(),
                                                ],
                                            style={"width": "15%"}
                                        ),
                                        html.Div(
                                            [
                                                platform_selector,
                                                ],
                                            style={"width": "10%"}
                                        ),
                                        html.Div(
                                            [
                                                date_picker
                                            ],
                                            style={"width": "15%"}
                                        ),
                                        html.Div(
                                            event_info_holder,
                                            style={"width": "60%"}
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        color_picker
                                    ],
                                ),
                                html.Div(
                                    [
                                        color_filter_style
                                    ],
                                    style={"width": "20%"}
                                ),
                                html.Br(),
                                html.H3("Data"),
                                general_stats,
                                event_graph,
                                dbc.Row(
                                    [
                                        html.Div(
                                            [
                                                html.H3("Color statistics"),
                                                color_pie
                                            ],
                                            style={"width": "50%"}
                                        ),
                                        html.Div(
                                            [
                                                html.H3("Splash statistics"),
                                                splash_pie
                                            ],
                                            style={"width": "50%"}
                                        )
                                    ]
                                )
                            ],
                        )
                    ]
                ),
            ]
        )
    ]
)


def get_color_emojis(color_string: str) -> str:
    emoji_string = ''
    for color_letter in color_string:
        emoji_string += emoji.emojize(f':{ColorNames[color_letter].value.lower()}_circle:')
    return emoji_string


@callback(
    Output(component_id='event-info-holder', component_property='children'),
    Input(component_id='events-data', component_property='hoverData')
)
def display_hover_data(hoverData):
    if not hoverData:
        return None
    returned_children = []
    data_to_parse = hoverData['points'][0]['hovertemplate'].split('<br>')
    for item in data_to_parse:
        if 'https' in item:
            returned_children.append(
                html.Div([
                html.A("Link", href=item.split()[1], target='_blank')
                ])
            )
        elif item.startswith('Color') or item.startswith('Splash'):
            item_parts = item.split()
            color_emojis = f'{item_parts[0]} {get_color_emojis(item_parts[1].strip())}'
            returned_children.append(color_emojis)
        else:
            returned_children.append(item)
        returned_children.append(html.Br())
    return html.Div(
        children=returned_children[:-1]
    )


@callback(
    [Output(component_id='events-data', component_property='figure'),
     Output(component_id='color-statistics', component_property='figure'),
     Output(component_id='splash-statistics', component_property='figure'),
     Output(component_id='general-stats', component_property='children')],
    [Input(component_id='format-selector', component_property='value'),
     Input(component_id='set-selector', component_property='value'),
     Input(component_id='platform-selector', component_property='value'),
     Input(component_id='date-picker', component_property='start_date'),
     Input(component_id='date-picker', component_property='end_date'),
     Input(component_id='color-picker', component_property='value'),
     Input(component_id='color-filter-style', component_property='value')]
)
def update_graphs(formats, set_display_names, platforms, start_date, end_date, colors, color_filter_style):
    filtered_df = df
    if platforms:
        filtered_df = filtered_df.query(f'platform == {platforms}')
    if formats:
        filtered_df = filtered_df.query(f'format == {formats}')
    chosen_set_codes = [re.search(r'\((.*?)\)', set_display_name).group(1) for set_display_name in set_display_names]
    if chosen_set_codes:
        filtered_df = filtered_df.query(f'set_code_name == {chosen_set_codes}')
    if colors:
        filtered_df = filter_colors(dataframe=filtered_df, colors=colors, color_filter_style=color_filter_style)

    if filtered_df.empty:
        return {}, {}, {}, "No data"

    filtered_df = filter_date_range(dataframe=filtered_df, start_date=start_date, end_date=end_date)

    if filtered_df.empty:
        return {}, {}, {}, "No data"

    data_fig = go.Figure()

    hovers = get_event_data(dataframe=filtered_df)
    data_fig.add_trace(
        go.Bar(
            x=filtered_df.display_date,
            y=filtered_df.wins,
            marker_color='#00CC96',
            name="Wins",
            showlegend=True,
            hovertemplate=hovers,
        )
    )
    data_fig.add_trace(
        go.Scatter(
            x=filtered_df.display_date,
            y=filtered_df.max_wins,
            mode='markers',
            marker_color='red',
            name="Max wins",
            showlegend=True,
            marker=dict(size=10, line=dict(width=2, color='Black')),
            opacity=0.8,
            hovertemplate=hovers
        )
    )
    data_fig.update_traces(marker_line_color='#636EFA', marker_line_width=1)

    color_statistics_fig = go.Figure()
    statistics = get_statistics(dataframe=filtered_df)
    color_statistics_fig.add_trace(
        go.Pie(
            labels=list(statistics["color_statistics"].keys()),
            values=list(statistics["color_statistics"].values()),
            sort=False,
            direction='clockwise',
            marker=dict(
                colors=[color.value for color in enums.ColorsRGBValues]
            )
        )
    )
    splash_statistics_fig = go.Figure()
    splash_statistics_fig.add_trace(
        go.Pie(
            labels=list(statistics["splash_statistics"].keys()),
            values=list(statistics["splash_statistics"].values()),
            sort=False,
            direction='clockwise',
            marker=dict(
                colors=[color.value for color in enums.ColorsRGBValues]
            )
        )
    )

    data_fig.update_xaxes(type='category', autotickangles=[0, 45, 90])
    general_statistics = get_general_statistics(dataframe=filtered_df, platforms=platforms)
    return data_fig, color_statistics_fig, splash_statistics_fig, general_statistics


if __name__ == '__main__':
    app.run(debug=True)
