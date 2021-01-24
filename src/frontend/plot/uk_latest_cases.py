import plotly.graph_objects as go
from src.fetch.visualise_nation_data import get_uk_data_latest
from src.frontend.colour.dash_colours import dash_colors


def uk_latest_graph():
    newCases, cumCases, date = get_uk_data_latest()
    return {
        'data': [{'type': 'indicator',
                  'mode': 'number',
                  'value': newCases,
                  'number': {'valueformat': ',',
                             'font': {'size': 30}},
                  'domain': {'y': [0, 1], 'x': [0, 1]}}],
        'layout': go.Layout(
            title={'text': "United Kingdom Confirmed Daily Cases - " + date},
            font=dict(color='black'),
            paper_bgcolor='white',
            plot_bgcolor=dash_colors['background'],
            height=200
        )
    }
