import pandas as pd
from pandas.core.frame import DataFrame
from magic_set import MagicSet, SetNames
from dash import html
from enums import ColorNames

def get_set_names_for_display(dataframe: DataFrame) -> list:
    set_code_names = dataframe['set_code_name'].drop_duplicates().to_list()[::-1]
    set_names_list = []
    for index in range(len(set_code_names)):
        set_object = MagicSet(set_code=set_code_names[index])
        set_names_list.append(set_object)
    return set_names_list


def get_multi_dropdown_data(dataframe: DataFrame) -> list:
    set_list = get_set_names_for_display(dataframe=dataframe)
    multi_dropdown_list = []
    for item in set_list:
        set_label = [
            html.Img(src=item.set_symbol_path, height=40, width=40, style={"padding-left": 10, "padding-bottom": 10}),
            html.Span(f'{item.set_name} ({item.set_code})', style={"font-size": 15, "padding-left": 10})
        ]
        set_value = f'{item.set_name} ({item.set_code})'
        multi_dropdown_list.append(
            {
                "label": set_label,
                "value": set_value
            }
        )
    return multi_dropdown_list


def get_event_data(dataframe: DataFrame):
    event_data_list = []
    for index, row in dataframe.iterrows():
        event_text = f'Set: {SetNames[row["set_code_name"]].value}<br>'
        event_text += f'Result: {row["result"]} ({row["platform"].title()})<br>'
        event_text += f'Colors: {row["colors"]}<br>'
        if type(row["splash"]) is str:
            event_text += f'Splash: {row["splash"]}<br>'
        event_text += f'Link: {row["link"]}'
        if not type(row["splash"]) is str:
            event_text += f'<br>'
        event_data_list.append(event_text)
    return event_data_list


def get_statistics(dataframe: DataFrame) -> dict:
    statistics = {
        "color_statistics": {color.value: 0 for color in ColorNames},
        "splash_statistics": {color.value: 0 for color in ColorNames}
    }
    for index, row in dataframe.iterrows():
        for color in ColorNames:
            if color.name in row["colors"]:
                statistics["color_statistics"][color.value] += 1
            if type(row["splash"]) is str and color.name in row["splash"]:
                statistics["splash_statistics"][color.value] += 1
    return statistics

def add_score_data(dataframe: DataFrame):
    max_wins = []
    result = []
    for row_index, row in dataframe.iterrows():
        if row["platform"] == "arena":
            max_wins.append(7)
        else:
            max_wins.append(row["wins"] + row["losses"] + row["ties"])
        if row["ties"] == 0:
            result.append(f'{row["wins"]}-{row["losses"]}')
        else:
            result.append(f'{row["wins"]}-{row["losses"]}-{row["ties"]}')
    dataframe = dataframe.assign(max_wins=max_wins)
    dataframe = dataframe.assign(result=result)
    return dataframe

def get_general_statistics(dataframe: DataFrame, platforms: str):
    if len(dataframe) == 0:
        return "No events found"
    total_wins = sum(dataframe["wins"])
    total_games = sum(dataframe["wins"]) + sum(dataframe["losses"]) + sum(dataframe["ties"])
    win_rate = round((total_wins / total_games) * 100, 2)

    splash_decks = dataframe["splash"].count()
    total_decks = len(dataframe)
    splash_rate = round((splash_decks / total_decks) * 100, 2)

    total_games_or_rounds_str = ''
    if 'arena' in platforms or not platforms:
        arena_events = dataframe.query(f"platform == {['arena']}")
        arena_games_count = sum(arena_events["wins"]) + sum(arena_events["losses"])
        total_games_or_rounds_str += f' | {len(arena_events)} Arena decks ({arena_games_count} games)'
    if 'paper' in platforms or not platforms:
        paper_events = dataframe.query(f"platform == {['paper']}")
        paper_matches_count = sum(paper_events["wins"]) + sum(paper_events["losses"]) + sum(paper_events["ties"])
        total_games_or_rounds_str += f' | {len(paper_events)} paper decks ({paper_matches_count} matches)'

    general_statistics = f'Overall win rate: {win_rate}% | Splash rate: {splash_rate}%{total_games_or_rounds_str} '
    return general_statistics


def get_color_pair_statistics(dataframe: DataFrame) -> DataFrame:
    grouped_df = dataframe.groupby('colors')[['wins', 'losses', 'ties']].sum()
    grouped_df['winrate'] = round(grouped_df['wins'] /
                                  (grouped_df['wins'] + grouped_df['losses'] + grouped_df['ties']) * 100, 2)
    return grouped_df.sort_values(by=['winrate'], ascending=False)

def filter_colors(dataframe: DataFrame, colors: list[str], color_filter_style: str) -> DataFrame:
    color_string = "".join(sorted(colors))
    if color_filter_style == "at_most":
        filtered_dataframe = dataframe[dataframe['colors'].apply(lambda x: set(x).issubset(color_string))]
        return filtered_dataframe
    if color_filter_style == "exactly":
        filtered_dataframe = dataframe[dataframe['colors'].apply(lambda x: ''.join(sorted(x)) == color_string)]
        return filtered_dataframe
    if color_filter_style == "including":
        filtered_dataframe = dataframe[dataframe['colors'].apply(lambda x: all(char in x for char in colors))]
        return filtered_dataframe

def add_date_formats(dataframe: DataFrame):
    dataframe['event_number'] = dataframe.groupby('date').cumcount() + 1
    dataframe['formatted_date'] = pd.to_datetime(dataframe['date'], format='%d/%m/%y')
    dataframe['display_date'] = dataframe['date']
    dataframe.loc[dataframe['date'].duplicated(keep=False), 'display_date'] = dataframe['date'] + ' (#' + dataframe['event_number'].astype(str) + ')'

def filter_date_range(dataframe: DataFrame, start_date, end_date) -> DataFrame:
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = dataframe[(dataframe['formatted_date'] >= start_date) & (dataframe['formatted_date'] <= end_date)]
    return filtered_df
