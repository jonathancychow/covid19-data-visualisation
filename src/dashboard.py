import plotly.graph_objects as go
from src.toolbox.SignalProcessing import moving_average
import math
from plotly.subplots import make_subplots
from src.fetch.visualise_region_data import get_region_data, get_region_data_today
from src.fetch.visualise_nation_data import get_nation_data, get_uk_data_latest
from src.fetch.visualise_country import get_country_data
import dash
import dash_core_components as dcc
import dash_html_components as html

dash_colors = {
    'background': '#111111',
    'text': '#BEBEBE',
    'grid': '#333333',
    'red': '#BF0000',
    'blue': '#466fc2',
    'green': '#5bc246',
    'black': '#000000'
}

fig1 = make_subplots(rows=1,
                    cols=3,
                    subplot_titles=('Confirmed Cases', 'Hospital Cases', 'New Admission')
                    )

nations = ['England']
# Row 1
for this_nation in nations:
    newCases, cumCases, date, hospitalCases, newAdmission = get_nation_data(this_nation)

    x = date
    data = [newCases,hospitalCases, newAdmission]

    col_count = 1
    for this_data in data:

        fig1.add_trace(go.Scatter(x = x, y = this_data,
                                mode = 'lines',
                                name = this_nation),
                                row=1,
                                col=col_count
                  )
        col_count += 1

fig1.update_layout(template="plotly_white",
                   showlegend=False,
                   title={
                       'text': "England Summary",
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'}
                   )

# Row 2
fig2 = go.Figure()
    # rows=1,
    #                  cols=3,
    #                  subplot_titles=('Country - Confirmed Cases', 'England Regional - Confirmed Cases'),
    #                  specs=[[{"colspan": 2}, None, {}]]
    #                  )

country = ['united-kingdom','spain', 'france','germany','belgium','italy']
status='confirmed'

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

fig6 = go.Figure()
area = ['Kingston Upon Thames','Richmond Upon Thames','Epsom and Ewell','Merton','Elmbridge']
for this_area in area:
    newCases, cumCases, date, df = get_region_data(this_area)

    x = date
    y = newCases
    N = 7
    y_mva = moving_average(df['newCasesByPublishDate'], N)

    fig6.add_trace(go.Scatter(x=df['date'][(math.ceil(N/2)):], y=y_mva,
                            mode='lines',
                            name=this_area),
                            # row = 1,
                            # col = 3
                  )
fig6.update_layout(template="plotly_white",
                   title={
                       'text': "England Regional - Confirmed Cases",
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'}
                   )

def kingston_confirmed():
    newCases, cumCases, death, date = get_region_data_today('Merton')
    # newCases, cumCases, death, date = get_region_data_today('Kingston Upon Thames')

    return {
            'data': [{'type': 'indicator',
                    'mode': 'number',
                    'value': newCases,
                    'number': {'valueformat': ',',
                              'font': {'size': 30}},
                    'domain': {'y': [0, 1], 'x': [0, 1]}}],
            'layout': go.Layout(
                title={'text': "Kingston Upon Thames Confirmed Cases - " + date},
                font=dict(color='black'),
                paper_bgcolor='white',
                plot_bgcolor=dash_colors['background'],
                height=200
                )
            }

fig3 = kingston_confirmed()

def kingston_cum_case():
    newCases, cumCases, death, date = get_region_data_today('Kingston Upon Thames')
    return {
            'data': [{'type': 'indicator',
                    'mode': 'number',
                    'value': cumCases,
                    'number': {'valueformat': ',',
                              'font': {'size': 30}},
                    'domain': {'y': [0, 1], 'x': [0, 1]}}],
            'layout': go.Layout(
                title={'text': "Kingston Upon Thames Cumulative Cases"},
                font=dict(color='black'),
                paper_bgcolor='white',
                plot_bgcolor=dash_colors['background'],
                height=200
                )
            }

fig4 = kingston_cum_case()

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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=external_stylesheets)
app.title = 'COVID-19-UK'
server = app.server

app.layout = html.Div(
    children=[
        html.Div(

            html.H1(children='COVID 19 Cases Dashboard',
                    style={
                        'textAlign': 'center',
                        'color': dash_colors['black'],
                        # 'backgroundColor': dash_colors['background'],
                    },
                    # className='ten columns',
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
            dcc.Graph(figure=fig6)],
            style={
                'textAlign': 'center',
                'color': dash_colors['text'],
                'width': '50%',
                'float': 'center',
                'display': 'inline-block'}

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

        html.Div(
            dcc.Graph(figure=fig4),
            style={
                'textAlign': 'center',
                'color': dash_colors['red'],
                'width': '33%',
                'float': 'left',
                'display': 'inline-block'
            }
        ),
        html.Div(
            dcc.Graph(figure=fig3),
            style={
                'textAlign': 'center',
                'color': dash_colors['red'],
                'width': '33%',
                'float': 'left',
                'display': 'inline-block'
            }
        ),
        html.Div([
            dcc.Graph(figure=fig1)],
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
        Source data: [UK Gov](https://coronavirus.data.gov.uk/) and [COVID 19 API](https://covid19api.com/)  
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


