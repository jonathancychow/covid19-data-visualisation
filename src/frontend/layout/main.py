import dash_html_components as html
import dash_core_components as dcc
from src.frontend.plot.vaccinated import vaccinated_graph
from src.frontend.plot.uk_latest_cases import uk_latest_graph
from src.frontend.colour.dash_colours import dash_colors


def main_layout():
    main_layout = html.Div(
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
                dcc.Graph(id='countries-graph')],
                style={
                    'textAlign': 'center',
                    'color': dash_colors['text'],
                    'width': '40%',
                    'float': 'center',
                    'display': 'inline-block'}

            ),
            html.Div([
                dcc.Graph(id='borough-graph'),
                dcc.Dropdown(
                    id='plot-borough-case',
                    multi=True,
                    options=[{'label': i, 'value': i}
                             for i in ['Kingston upon Thames', 'Richmond upon Thames', 'Epsom and Ewell',
                                       'Merton', 'Sutton', 'Elmbridge', 'Surrey Heath',
                                       'Mole Valley', 'Guildford',
                                       'Reigate and Banstead', 'Woking', 'Gravesham',
                                       'Hammersmith and Fulham']],
                    value=['Kingston upon Thames', 'Richmond upon Thames', 'Epsom and Ewell'],
                    style={
                        'fontSize': 15,
                        'width': '100%',
                        'display': 'inline-block',
                        'verticalAlign': "middle",
                    },
                )
            ],
                style={
                    'textAlign': 'center',
                    'color': dash_colors['text'],
                    'width': '40%',
                    'float': 'center',
                    'display': 'inline-block'}

            ),
            html.Div([
                dcc.Graph(figure=vaccinated_graph())],
                style={
                    'textAlign': 'center',
                    'color': dash_colors['text'],
                    'width': '20%',
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
                                               'Merton', 'Sutton', 'Elmbridge', 'Surrey Heath',
                                               'Mole Valley', 'Guildford',
                                               'Reigate and Banstead', 'Woking', 'Gravesham',
                                               'Hammersmith and Fulham']],
                            value='Kingston upon Thames',
                            style={
                                'fontSize': 15,
                                'width': '100%',
                                'display': 'inline-block',
                                'verticalAlign': "middle",
                            },
                        )
                    ),
                    html.Label(
                        dcc.RadioItems(
                            id='unit-conversion-borough',
                            options=[{'label': i, 'value': i}
                                     for i in ['Absolute', 'Per 100,000']],
                            value='Absolute',
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
                dcc.Graph(figure=uk_latest_graph()),
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
                                 for i in ['England', 'Wales', 'Scotland', 'Northern Ireland']],
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
                                 for i in ['Absolute', 'Per 100,000']],
                        value='Absolute',
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
            
            Source data: [UK Gov](https://coronavirus.data.gov.uk/), [COVID 19 API](https://covid19api.com/), [Datahub](https://datahub.io/core/population#data) and [ONS](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/populationestimatesforukenglandandwalesscotlandandnorthernireland)
            
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
    return main_layout
