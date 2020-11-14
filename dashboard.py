import plotly.graph_objects as go
from SignalProcessing import moving_average
from uk_covid19 import Cov19API
import math
from plotly.subplots import make_subplots
from visualise_region_data import get_region_data
from visualise_nation_data import get_nation_data

fig = make_subplots(rows=3,
                    cols=2,
                    subplot_titles=('Confirmed Cases', 'Region Data - 7 Days Average', 'Hospital Cases', 'New Admission'),
                    specs=[[{}, {"rowspan": 3}],
                           [{}, None],
                           [{}, None]]
                    )

nations = ['England', 'Wales', 'Scotland', 'Northern Ireland']
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
                            row = 1,
                            col = 2
                  )

fig.show()