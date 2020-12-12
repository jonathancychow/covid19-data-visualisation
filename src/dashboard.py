import plotly.graph_objects as go
from src.toolbox.SignalProcessing import moving_average
import math
from plotly.subplots import make_subplots
from src.fetch.visualise_region_data import get_region_data, get_region_data_today
from src.fetch.visualise_nation_data import get_nation_data, get_uk_data_latest
from src.fetch.visualise_country import get_country_data
from src.fetch.get_population import case_density_conversion, get_population_df
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

dash_colors = {
    'background': '#111111',
    'text': '#BEBEBE',
    'grid': '#333333',
    'red': '#BF0000',
    'blue': '#466fc2',
    'green': '#5bc246',
    'black': '#000000'
}
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=external_stylesheets)
app.title = 'COVID-19-UK'
server = app.server


df= get_population_df()
print(df)

@app.callback(
    Output('uk-nation-graph', 'figure'),
    [Input('regional-input', 'value'),
     Input('unit-conversion-nation','value')])
def uk_nation(nation, unit):
    newCases, cumCases, date, hospitalCases, newAdmission = get_nation_data(nation)
    if unit == 'Per 100,000':
        newCases = case_density_conversion(newCases, nation.upper())
        hospitalCases = case_density_conversion(hospitalCases, nation.upper())
        newAdmission = case_density_conversion(newAdmission, nation.upper())

    x = date
    return {
        'data': [{'mode': 'lines',
                  'name': 'England',
                  'type': 'scatter',
                  'x': x,
                  'xaxis': 'x',
                  'y': newCases,
                  'yaxis': 'y'},
                 {'mode': 'lines',
                  'name': 'England',
                  'type': 'scatter',
                  'x': x,
                  'xaxis': 'x2',
                  'y': hospitalCases,
                  'yaxis': 'y2'},
                 {'mode': 'lines',
                  'name': 'England',
                  'type': 'scatter',
                  'x': x,
                  'xaxis': 'x3',
                  'y': newAdmission,
                  'yaxis': 'y3'}],
        'layout': {'annotations': [{'font': {'size': 16},
                                    'showarrow': False,
                                    'text': 'Confirmed Cases',
                                    'x': 0.14444444444444446,
                                    'xanchor': 'center',
                                    'xref': 'paper',
                                    'y': 1.0,
                                    'yanchor': 'bottom',
                                    'yref': 'paper'},
                                   {'font': {'size': 16},
                                    'showarrow': False,
                                    'text': 'Hospital Cases',
                                    'x': 0.5,
                                    'xanchor': 'center',
                                    'xref': 'paper',
                                    'y': 1.0,
                                    'yanchor': 'bottom',
                                    'yref': 'paper'},
                                   {'font': {'size': 16},
                                    'showarrow': False,
                                    'text': 'New Admission',
                                    'x': 0.8555555555555556,
                                    'xanchor': 'center',
                                    'xref': 'paper',
                                    'y': 1.0,
                                    'yanchor': 'bottom',
                                    'yref': 'paper'}],
                   'showlegend': False,
                   'template': '...',
                   'title': {'text': nation + ' Summary', 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                   'xaxis': {'anchor': 'y', 'domain': [0.0, 0.2888888888888889]},
                   'xaxis2': {'anchor': 'y2', 'domain': [0.35555555555555557, 0.6444444444444445]},
                   'xaxis3': {'anchor': 'y3', 'domain': [0.7111111111111111, 1.0]},
                   'yaxis': {'anchor': 'x', 'domain': [0.0, 1.0]},
                   'yaxis2': {'anchor': 'x2', 'domain': [0.0, 1.0]},
                   'yaxis3': {'anchor': 'x3', 'domain': [0.0, 1.0]}}
    }


fig2 = go.Figure()
country = ['United-Kingdom', 'Spain', 'France', 'Germany', 'Italy']
status = 'confirmed'

for thisCountry in country:
    date, cumulativeCase, dailyCase = get_country_data(thisCountry, status)

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
                       'text': "Europe - Confirmed Cases",
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'}
                   )


@app.callback(
    Output('borough-graph', 'figure'),
    [Input('graph-type', 'value'),
     Input('unit-conversion-borough', 'value')])
def borough_graph(borough, unit):
    fig6 = go.Figure()
    area = ['Kingston upon Thames','Richmond upon Thames','Epsom and Ewell','Merton','Elmbridge']
    for this_area in area:
        newCases, cumCases, date, df = get_region_data(this_area)

        x = date
        y = newCases
        N = 7
        y_mva = moving_average(df['newCasesByPublishDate'], N)
        if unit == 'Per 100,000':
            y_mva = case_density_conversion(y_mva, this_area)

        fig6.add_trace(go.Scatter(x=df['date'][(math.ceil(N/2)):], y=y_mva,
                                mode='lines',
                                name=this_area),
                                # row = 1,
                                # col = 3
                      )
    fig6.update_layout(template="plotly_white",
                       title={
                           'text': "Surrey - Confirmed Cases",
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
    print('confirm case - ', borough)
    newCases, cumCases, death, date = get_region_data_today(borough)
    if unit == 'Per 100,000':
        newCases = case_density_conversion(newCases, borough)
    return {
            'data': [{'type': 'indicator',
                    'mode': 'number',
                    'value': newCases,
                    'number': {'valueformat': ',',
                              'font': {'size': 30}},
                    'domain': {'y': [0, 1], 'x': [0, 1]}}],
            'layout': go.Layout(
                # title={'text': "Kingston Upon Thames Confirmed Cases - " + date},
                title={'text': borough + " Confirmed Cases - " + date},
                font=dict(color='black'),
                paper_bgcolor='white',
                plot_bgcolor=dash_colors['background'],
                height=200
                )
            }

@app.callback(
    Output('graph-cum-case', 'figure'),
    [Input('graph-type', 'value'),
     Input('unit-conversion-borough','value')])
def kingston_cum_case(borough, unit):
    newCases, cumCases, death, date = get_region_data_today(borough)
    if unit == 'Per 100,000':
        cumCases = case_density_conversion(cumCases, borough)
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

def uk_latest():
    newCases, cumCases, date = get_uk_data_latest()
    return {
            'data': [{'type': 'indicator',
                      'mode': 'number',
                      'value': newCases,
                    'number': {'valueformat': ',',
                              'font': {'size': 30}},
                    'domain': {'y': [0, 1], 'x': [0, 1]}}],
            'layout': go.Layout(
                title={'text': "United Kingdom Confirmed Cases - " + date},
                font=dict(color='black'),
                paper_bgcolor='white',
                plot_bgcolor=dash_colors['background'],
                height=200
                )
            }

fig5 = uk_latest()

app.layout = html.Div(
    children=[
        html.Div(

            html.H1(children='COVID 19 Cases Dashboard',
                    style={
                        'textAlign': 'center',
                        'color': dash_colors['black'],
                    },
                    )
        ),

        html.Div([
            dcc.Graph(figure=fig2)],
            style={
                'textAlign': 'center',
                'color': dash_colors['text'],
                'width': '50%',
                'float': 'center',
                'display': 'inline-block'}

        ),
        html.Div([
            dcc.Graph(id='borough-graph')],
            style={
                'textAlign': 'center',
                'color': dash_colors['text'],
                'width': '50%',
                'float': 'center',
                'display': 'inline-block'}

        ),
        html.Div(
            dcc.Graph(id='graph-cum-case'),
            style={
                'textAlign': 'center',
                'color': dash_colors['red'],
                'width': '33%',
                'float': 'left',
                'display': 'inline-block'
            }
        ),
        html.Div(
            children=[
                html.Label(dcc.Graph(id='graph-confirm')),
                html.Label(
                    dcc.Dropdown(
                        id='graph-type',
                        options=[{'label': i, 'value': i}
                                 for i in ['Kingston upon Thames', 'Richmond upon Thames', 'Epsom and Ewell',
                                           'Merton', 'Elmbridge', 'Mole Valley', 'Guildford', 'Woking', 'Gravesham',
                                           'Hammersmith and Fulham']],
                        value='Kingston upon Thames',
                        style={
                            'fontSize': 15,
                            'width': '100%',
                            'display': 'inline-block',
                            'verticalAlign': "middle",
                        },
                    )),
                html.Label(
                    dcc.RadioItems(
                        id='unit-conversion-borough',
                        options=[{'label': i, 'value': i}
                                 for i in ['Absoluate', 'Per 100,000']],
                        value='Absoluate',
                        style={
                            'fontSize': 15,
                            'width': '33%',
                            'display': 'inline-block',
                            'verticalAlign': "middle",
                        },
                    ))
            ],
            style={
                'textAlign': 'center',
                'color': dash_colors['black'],
                'width': '33%',
                'float': 'left',
                'display': 'inline-block'
            }
        ),
        html.Div(
            dcc.Graph(figure=fig5),
            style={
                'textAlign': 'center',
                'color': dash_colors['red'],
                'width': '33%',
                'float': 'left',
                'display': 'inline-block'
            }
        ),
        html.Div([
            html.Label(dcc.Graph(id='uk-nation-graph')),
            html.Label(
                dcc.Dropdown(
                    id='regional-input',
                    options=[{'label': i, 'value': i}
                             for i in ['England', 'Wales', 'Scotland','Northern Ireland']],
                    value='England',
                    style={
                        'fontSize': 15,
                        'width': '33%',
                        'display': 'inline-block',
                        'verticalAlign': "middle",
                    },
                )),
            html.Label(
                dcc.RadioItems(
                    id='unit-conversion-nation',
                    options=[{'label': i, 'value': i}
                             for i in ['Absoluate', 'Per 100,000']],
                    value='Absoluate',
                    style={
                        'fontSize': 15,
                        'width': '33%',
                        'display': 'inline-block',
                        'verticalAlign': "middle",
                    },
                ))
        ],
            style={
                'textAlign': 'center',
                'color': dash_colors['text'],
                'width': '100%',
                'float': 'center',
                'display': 'inline-block'}

        ),
        html.Div(dcc.Markdown('''
        &nbsp;  
        &nbsp;  
        Built by [Jonathan Chow](https://www.linkedin.com/in/jonathan-chow-b370b276/)  
        
        Source data: [UK Gov](https://coronavirus.data.gov.uk/), [COVID 19 API](https://covid19api.com/) and [ONS](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/populationestimatesforukenglandandwalesscotlandandnorthernireland)
        
        Documention [here](https://github.com/jonathancychow/covid19-data-visualisation)  
        '''),
                 style={
                     'textAlign': 'center',
                     'color': dash_colors['text'],
                     'width': '100%',
                     'float': 'center',
                     'display': 'inline-block'}
                 )
    ])

if __name__ == '__main__':
    app.run_server(debug=True)


