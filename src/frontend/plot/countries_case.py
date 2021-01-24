from src.toolbox.SignalProcessing import moving_average
from src.fetch.visualise_country import get_country_data
import plotly.graph_objects as go


def countries_case_graph(country, unit):
    fig = go.Figure()
    status = 'confirmed'
    for thisCountry in country:
        date, cumulativeCase, dailyCase = get_country_data(thisCountry, status)
        if unit == 'Per 100,000':
            global countries_population_df
            dailyCase = [100000 * x / countries_population_df[thisCountry] for x in dailyCase]
        x = date
        y = dailyCase
        N = 7
        y_mva = moving_average(dailyCase, N)

        fig.add_trace(go.Scatter(x=date, y=y_mva,
                                 mode='lines',
                                 name=thisCountry)
                      )
    fig.update_layout(template="plotly_white",
                      title={
                          'text': "Europe - Confirmed Daily Cases",
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'}
                      )
    return fig
