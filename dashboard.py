import plotly.graph_objects as go
from SignalProcessing import moving_average
from uk_covid19 import Cov19API
import math
from plotly.subplots import make_subplots
from visualise_region_data import get_nation_data
from visualise_nation_data import get_nation_data

fig = make_subplots(rows=3, cols=2, subplot_titles=('Confirmed Cases', 'Hospital Cases', 'New Admission'))

nations = ['England', 'Wales', 'Scotland', 'Northern Ireland']
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





fig.show()