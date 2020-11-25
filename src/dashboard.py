import plotly.graph_objects as go
from src.toolbox.SignalProcessing import moving_average
import math
from plotly.subplots import make_subplots
from src.fetch.visualise_region_data import get_region_data
from src.fetch.visualise_nation_data import get_nation_data
from src.fetch.visualise_country import get_country_data
import dash
import dash_core_components as dcc
import dash_html_components as html

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
fig2 = make_subplots(rows=1,
                     cols=3,
                     subplot_titles=('Country - Confimred Cases', 'England Regional - Confirmed Cases'),
                     specs=[[{"colspan": 2}, None, {}]]
                     )

country = ['united-kingdom','spain', 'france','germany','korea-south']
status='confirmed'

for thisCountry in country:
    date, cumulativeCase, dailyCase = get_country_data(thisCountry, status)

    x = date
    y= dailyCase
    N = 7
    y_mva = moving_average(dailyCase, N)

    fig2.add_trace(go.Scatter(x=date,y=y_mva,
                                 mode='lines',
                                 name=thisCountry),
                                 row=1,
                                 col=1)

area = ['Kingston Upon Thames','Richmond Upon Thames','Epsom and Ewell','Hackney and City of London']
for this_area in area:
    newCases, cumCases, date, df = get_region_data(this_area)

    x = date
    y = newCases
    N = 7
    y_mva = moving_average(df['newCasesByPublishDate'], N)

    fig2.add_trace(go.Scatter(x=df['date'][(math.ceil(N/2)):], y=y_mva,
                            mode='lines',
                            name=this_area),
                            row = 1,
                            col = 3
                  )


fig2.update_layout(template="plotly_white",
                   title={
                       'text': "COVID 19 Cases Dashboard",
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top'}
                   )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    children=[
# html.H1(children='COVID 19 Cases Dashboard'),
        html.Div([
            dcc.Graph(figure=fig2, style={'height': '45vh'})]),
        html.Div([
            dcc.Graph(figure=fig1, style={'height': '45vh'})])
    ])

if __name__ == '__main__':
    app.run_server(debug=True)


