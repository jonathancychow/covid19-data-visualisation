import plotly.graph_objects as go
from src.fetch.visualise_nation_data import get_uk_vaccinated

def vaccinated_graph():
    fig7 = go.Figure()

    vaccinated, date = get_uk_vaccinated()

    x = date
    y = vaccinated
        # N = 7
        # y_mva = moving_average(df['newCasesByPublishDate'], N)
        # if unit == 'Per 100,000':
        #     global population_df
        #     y_mva = case_density_conversion(y_mva, this_area, population_df)

    fig7.add_trace(go.Scatter(x=date, y=y,
                                  mode='lines',
                                  ),
                       )
    fig7.update_layout(template="plotly_white",
                       title={
                           'text': "UK - Daily People Vaccinated",
                           'x': 0.5,
                           'xanchor': 'center',
                           'yanchor': 'top'}
                       )
    fig7.update_xaxes(
        tickformat="%b %d")
    return fig7