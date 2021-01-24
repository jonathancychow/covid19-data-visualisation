from src.toolbox.SignalProcessing import moving_average
from src.fetch.visualise_region_data import get_region_data
import math
import plotly.graph_objects as go
from src.fetch.get_population import case_density_conversion, get_borough_population_df, get_countries_population_df

population_df = get_borough_population_df()

def borough_case_graph(borough, unit):
    fig6 = go.Figure()

    for this_area in borough:
        newCases, cumCases, date, df = get_region_data(this_area)

        x = date
        y = newCases
        N = 7
        y_mva = moving_average(df['newCasesByPublishDate'], N)
        if unit == 'Per 100,000':
            global population_df
            y_mva = case_density_conversion(y_mva, this_area, population_df)

        fig6.add_trace(go.Scatter(x=df['date'][(math.ceil(N / 2)):], y=y_mva,
                                  mode='lines',
                                  name=this_area),
                       )
    fig6.update_layout(template="plotly_white",
                       title={
                           'text': "Surrey - Confirmed Daily Cases",
                           'x': 0.5,
                           'xanchor': 'center',
                           'yanchor': 'top'}
                       )
    return fig6
