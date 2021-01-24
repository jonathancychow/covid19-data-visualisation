import plotly.graph_objects as go
from plotly.subplots import make_subplots


def uk_nation_layout(nation, date, vaccinated_date, newCases, hospitalCases, newAdmission, vaccinated):
    fig = make_subplots(rows=1,
                         cols=4,
                         subplot_titles=('Confirmed Cases', 'Hospital Cases', 'New Admission', 'Vaccinated')
                         )

    fig.add_trace(go.Scatter(x=date, y=newCases,
                              mode='lines',
                              name=nation),
                   row=1,
                   col=1
                   )
    fig.add_trace(go.Scatter(x=date, y=hospitalCases,
                              mode='lines',
                              name=nation),
                   row=1,
                   col=2
                   )
    fig.add_trace(go.Scatter(x=date, y=newAdmission,
                              mode='lines',
                              name=nation),
                   row=1,
                   col=3
                   )
    fig.add_trace(go.Scatter(x=vaccinated_date, y=vaccinated,
                              mode='lines',
                              name=nation),
                   row=1,
                   col=4
                   )

    fig.update_layout(template="plotly_white",
                       showlegend=False,
                       title={
                           'text': nation + " Summary",
                           'x': 0.5,
                           'xanchor': 'center',
                           'yanchor': 'top'}
                       )
    return fig
