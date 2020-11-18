from requests import get
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
from uk_covid19 import Cov19API


def get_nation_data(nation):
    england_only = [
        'areaType=nation',
        'areaName=England'
    ]
    all_nations = [
        "areaType=nation"
    ]
    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumCasesByPublishDate": "cumCasesByPublishDate",
        "newDeathsByDeathDate": "newDeathsByDeathDate",
        "cumDeathsByDeathDate": "cumDeathsByDeathDate",
        "hospitalCases": "hospitalCases",
        "newAdmissions": "newAdmissions"
    }
    nation_filter = [
        'areaType=nation',
        'areaName=' + nation
    ]
    api = Cov19API(filters=nation_filter, structure=cases_and_deaths)

    data = api.get_json()
    cumCases = []
    date = []
    newCases = []
    hospitalCases = []
    newAdmission = []
    for case in data['data']:
        cumCases.append(case['cumCasesByPublishDate'])
        date.append(case['date'])
        newCases.append(case['newCasesByPublishDate'])
        hospitalCases.append((case['hospitalCases']))
        newAdmission.append(case['newAdmissions'])

    return newCases, cumCases, date, hospitalCases, newAdmission

if __name__ == '__main__':
    # fig = go.Figure()
    fig = make_subplots(rows=3, cols=1,subplot_titles=('Confirmed Cases','Hospital Cases', 'New Admission'))

    nations = ['England','Wales','Scotland','Northern Ireland']
    for this_nation in nations:
        newCases, cumCases, date, hospitalCases, newAdmission = get_nation_data(this_nation)

        x = date
        y = newCases

        fig.add_trace(go.Scatter(x=x, y=y,
                                 mode='lines',
                                 name=this_nation),
                                 row=1,
                                 col=1
                      )
        y = hospitalCases
        fig.add_trace(go.Scatter(x=x, y=y,
                                 mode='lines',
                                 name=this_nation),
                                 row=2,
                                 col=1
                      )
        y = newAdmission
        fig.add_trace(go.Scatter(x=x, y=y,
                                 mode='lines',
                                 name=this_nation),
                      row=3,
                      col=1
                      )

    fig.show()