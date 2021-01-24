from src.fetch.visualise_region_data import get_region_data_today
from src.fetch.visualise_nation_data import get_nation_data
from src.fetch.get_population import case_density_conversion, get_borough_population_df
import dash
from dash.dependencies import Input, Output
from src.frontend.layout.main import main_layout
from src.frontend.layout.borough_cum_case import borough_cum_case_layout
from src.frontend.layout.borough_daily_case import borough_daily_case_layout
from src.frontend.layout.uk_nation import uk_nation_layout
from src.frontend.plot.countries_case import countries_case_graph
from src.frontend.plot.borough_case import borough_case_graph

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=external_stylesheets)
app.title = 'COVID-19-UK'
server = app.server
population_df = get_borough_population_df()


@app.callback(
    Output('uk-nation-graph', 'figure'),
    [Input('regional-input', 'value'),
     Input('unit-conversion-nation', 'value')])
def uk_nation(nation, unit):
    newCases, cumCases, date, hospitalCases, newAdmission, vaccinated, vaccinated_date = get_nation_data(nation)
    if unit == 'Per 100,000':
        global population_df
        newCases = case_density_conversion(newCases, nation.upper(), population_df)
        hospitalCases = case_density_conversion(hospitalCases, nation.upper(), population_df)
        newAdmission = case_density_conversion(newAdmission, nation.upper(), population_df)
        vaccinated = case_density_conversion(vaccinated, nation.upper(), population_df)
    return uk_nation_layout(nation, date, vaccinated_date, newCases, hospitalCases, newAdmission, vaccinated)


@app.callback(
    Output('countries-graph', 'figure'),
    [Input('unit-conversion-borough', 'value'),
     Input('plot-countries-case', 'value')
     ])
def plot_countries(unit, countries):
    return countries_case_graph(countries, unit)


@app.callback(
    Output('borough-graph', 'figure'),
    [Input('plot-borough-case', 'value'),
     Input('unit-conversion-borough', 'value')])
def borough_graph(borough, unit):
    return borough_case_graph(borough, unit)


@app.callback(
    Output('graph-confirm', 'figure'),
    [Input('graph-type', 'value'),
     Input('unit-conversion-borough', 'value')])
def borough_confirmed(borough, unit):
    newCases, cumCases, death, date = get_region_data_today(borough)
    if unit == 'Per 100,000':
        global population_df
        newCases = case_density_conversion(newCases, borough, population_df)
    return borough_daily_case_layout(newCases, borough, date)


@app.callback(
    Output('graph-cum-case', 'figure'),
    [Input('graph-type', 'value'),
     Input('unit-conversion-borough', 'value')])
def borough_cum_case(borough, unit):
    newCases, cumCases, death, date = get_region_data_today(borough)
    if unit == 'Per 100,000':
        global population_df
        cumCases = case_density_conversion(cumCases, borough, population_df)
    return borough_cum_case_layout(cumCases, borough)


app.layout = main_layout()

if __name__ == '__main__':
    app.run_server(debug=True)
