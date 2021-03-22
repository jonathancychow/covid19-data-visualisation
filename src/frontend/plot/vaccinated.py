import plotly.graph_objects as go
from src.fetch.visualise_nation_data import get_uk_vaccinated
from src.toolbox.SignalProcessing import moving_average


def vaccinated_graph():
    fig = go.Figure()

    vaccinated, date = get_uk_vaccinated()

    x = date
    y = vaccinated
    N = 7
    y_mva = moving_average(y, N)
    
    fig.add_trace(go.Scatter(x=date, y=y_mva,
                              mode='lines',
                              ),
                   )
    fig.update_layout(template="plotly_white",
                       title={
                           'text': "UK - Daily People Vaccinated",
                           'x': 0.5,
                           'xanchor': 'center',
                           'yanchor': 'top'}
                       )
    fig.update_xaxes(
        tickformat="%b %d")
    return fig
