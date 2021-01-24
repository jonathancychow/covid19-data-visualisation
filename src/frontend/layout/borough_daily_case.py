from src.frontend.colour.dash_colours import dash_colors
import plotly.graph_objects as go

def borough_daily_case_layout(newCases, borough, date):
    return {
        'data': [{'type': 'indicator',
                  'mode': 'number',
                  'value': newCases,
                  'number': {'valueformat': ',',
                             'font': {'size': 30}},
                  'domain': {'y': [0, 1], 'x': [0, 1]}}],
        'layout': go.Layout(
            title={'text': borough + " Confirmed Daily Cases - " + date},
            font=dict(color='black'),
            paper_bgcolor='white',
            plot_bgcolor=dash_colors['background'],
            height=200
        )
    }