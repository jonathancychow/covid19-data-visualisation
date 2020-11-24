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

fig = make_subplots(rows=3,
                    cols=2,
                    subplot_titles=('England - Confirmed Cases', 'Country Data - 7 Days Average', 'England - Hospital Cases', 'England - New Admission','England Regional Data - 7 Days Average'),
                    specs=[[{}, {"rowspan": 2}],
                           [{}, None],
                           [{}, {}]]
                    )

nations = ['England']
# Column 1
for this_nation in nations:
    newCases, cumCases, date, hospitalCases, newAdmission = get_nation_data(this_nation)

    x = date
    data = [newCases,hospitalCases, newAdmission]

    row_count = 1
    for this_data in data:

        fig.add_trace(go.Scatter(x = x, y = this_data,
                                mode = 'lines',
                                name = this_nation),
                                row=row_count,
                                col=1
                  )
        row_count += 1

# column 2
country = ['united-kingdom','spain', 'france','germany','korea-south']
status='confirmed'
    # fig = make_subplots(rows=2, cols=1,subplot_titles=('Confirmed Cases','Deaths'))

for thisCountry in country:
    date, cumulativeCase, dailyCase = get_country_data(thisCountry, status)

    x = date
    y= dailyCase
    N = 7
    y_mva = moving_average(dailyCase, N)

    fig.add_trace(go.Scatter(x=date,y=y_mva,
                                 mode='lines',
                                 name=thisCountry),
                                 row=1,
                                 col=2)

area = ['Kingston Upon Thames','Richmond Upon Thames','Epsom and Ewell','Hackney and City of London']
for this_area in area:
    newCases, cumCases, date, df = get_region_data(this_area)

    x = date
    y = newCases
    N = 7
    y_mva = moving_average(df['newCasesByPublishDate'], N)

    fig.add_trace(go.Scatter(x=df['date'][(math.ceil(N/2)):], y=y_mva,
                            mode='lines',
                            name=this_area),
                            row = 3,
                            col = 2
                  )

fig.update_layout(template = "plotly_dark", title="COVID 19 Cases Dashboard ")
# fig.show()


app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter



