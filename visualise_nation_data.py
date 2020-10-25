from requests import get
import plotly.graph_objects as go
import numpy as np
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
        "cumDeathsByDeathDate": "cumDeathsByDeathDate"
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
    for case in data['data']:
        cumCases.append(case['cumCasesByPublishDate'])
        date.append(case['date'])
        newCases.append(case['newCasesByPublishDate'])

    return newCases, cumCases, date

if __name__ == '__main__':
    fig = go.Figure()
    nations = ['England','Wales','Scotland','Northern Ireland']
    for this_nation in nations:
        newCases, cumCases, date = get_nation_data(this_nation)

        x = date
        y= newCases

        fig.add_trace(go.Scatter(x=date, y=newCases,
                                 mode='lines',
                                 name=this_nation))
    fig.show()