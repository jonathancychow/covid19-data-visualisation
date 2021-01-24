from src.frontend.colour.dash_colours import dash_colors
import plotly.graph_objects as go


def borough_cum_case_layout(cumCases, borough):
    return {
        'data': [{'type': 'indicator',
                  'mode': 'number',
                  'value': cumCases,
                  'number': {'valueformat': ',',
                             'font': {'size': 30}},
                  'domain': {'y': [0, 1], 'x': [0, 1]}}],
        'layout': go.Layout(
            title={'text': borough + " Cumulative Cases"},
            font=dict(color='black'),
            paper_bgcolor='white',
            plot_bgcolor=dash_colors['background'],
            height=200
        )
    }
