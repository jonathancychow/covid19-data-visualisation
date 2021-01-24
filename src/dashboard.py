import plotly.graph_objects as go
from src.toolbox.SignalProcessing import moving_average
import math
from plotly.subplots import make_subplots
from src.fetch.visualise_region_data import get_region_data, get_region_data_today
from src.fetch.visualise_nation_data import get_nation_data, get_uk_data_latest, get_uk_vaccinated
from src.fetch.visualise_country import get_country_data
from src.fetch.get_population import case_density_conversion, get_borough_population_df, get_countries_population_df
import dash
from dash.dependencies import Input, Output
from src.frontend.layout.main import main_layout
from src.frontend.colour.dash_colours import dash_colors
from src.frontend.layout.borough_cum_case import borough_cum_case_layout
from src.frontend.layout.borough_daily_case import borough_daily_case_layout

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=external_stylesheets)
app.title = 'COVID-19-UK'
server = app.server
population_df = get_borough_population_df()
countries_population_df = get_countries_population_df()

@app.callback(
    Output('uk-nation-graph', 'figure'),
    [Input('regional-input', 'value'),
     Input('unit-conversion-nation','value')])
def uk_nation(nation, unit):
    newCases, cumCases, date, hospitalCases, newAdmission, vaccinated, vaccinated_date = get_nation_data(nation)
    if unit == 'Per 100,000':
        global population_df
        newCases = case_density_conversion(newCases, nation.upper(), population_df)
        hospitalCases = case_density_conversion(hospitalCases, nation.upper(), population_df)
        newAdmission = case_density_conversion(newAdmission, nation.upper(), population_df)
        vaccinated = case_density_conversion(vaccinated, nation.upper(), population_df)

    fig1 = make_subplots(rows=1,
                         cols=4,
                         subplot_titles=('Confirmed Cases', 'Hospital Cases', 'New Admission', 'Vaccinated')
                         )
    x = date
    data = [newCases, hospitalCases, newAdmission, vaccinated]

    col_count = 1
    for this_data in data:
        if col_count == 4:
            # mode = 'lines+markers'
            mode = 'markers'
            mode = 'lines'
            x = vaccinated_date

        else:
            mode = 'lines'
        fig1.add_trace(go.Scatter(x=x, y=this_data,
                                  mode=mode,
                                  name=nation),
                       row=1,
                       col=col_count
                       )
        col_count += 1
    fig1.update_layout(template="plotly_white",
                       showlegend=False,
                       title={
                           'text': nation + " Summary",
                           'x': 0.5,
                           'xanchor': 'center',
                           'yanchor': 'top'}
                       )
    return fig1

@app.callback(
    Output('countries-graph', 'figure'),
     Input('unit-conversion-borough','value'))
def plot_countries(unit):
    fig2 = go.Figure()
    country = ['United-Kingdom', 'Spain', 'France', 'Germany', 'Italy']
    status = 'confirmed'

    for thisCountry in country:
        date, cumulativeCase, dailyCase = get_country_data(thisCountry, status)
        if unit == 'Per 100,000':
            global countries_population_df
            dailyCase = [100000 * x / countries_population_df[thisCountry] for x in dailyCase ]

        x = date
        y= dailyCase
        N = 7
        y_mva = moving_average(dailyCase, N)

        fig2.add_trace(go.Scatter(x=date,y=y_mva,
                                     mode='lines',
                                     name=thisCountry)
                       )
    fig2.update_layout(template="plotly_white",
                       title={
                           'text': "Europe - Confirmed Daily Cases",
                           'x': 0.5,
                           'xanchor': 'center',
                           'yanchor': 'top'}
                       )
    return fig2


@app.callback(
    Output('borough-graph', 'figure'),
    [Input('plot-borough-case','value'),
     Input('unit-conversion-borough', 'value')])
def borough_graph(borough, unit):
    fig6 = go.Figure()
    area = borough

    for this_area in area:
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

@app.callback(
    Output('graph-confirm', 'figure'),
    [Input('graph-type', 'value'),
     Input('unit-conversion-borough','value')])
def borough_confirmed(borough, unit):
    newCases, cumCases, death, date = get_region_data_today(borough)
    if unit == 'Per 100,000':
        global population_df
        newCases = case_density_conversion(newCases, borough, population_df)
    return borough_daily_case_layout(newCases, borough, date)

@app.callback(
    Output('graph-cum-case', 'figure'),
    [Input('graph-type', 'value'),
     Input('unit-conversion-borough','value')])
def kingston_cum_case(borough, unit):
    newCases, cumCases, death, date = get_region_data_today(borough)
    if unit == 'Per 100,000':
        global population_df
        cumCases = case_density_conversion(cumCases, borough, population_df)
    return borough_cum_case_layout(cumCases, borough)

app.layout = main_layout()

if __name__ == '__main__':
    app.run_server(debug=True)


