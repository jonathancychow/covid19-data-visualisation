from requests import get
import plotly.graph_objects as go
import numpy as np
from uk_covid19 import Cov19API
import plotly.express as px

def get_nation_data(area):
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
    area_filter = [
        'areaName='+ area + '&'
    ]
    api = Cov19API(filters=area_filter, structure=cases_and_deaths)
    # api = Cov19API(filters=all_nations, structure=cases_and_deaths, latest_by="newCasesByPublishDate")
    # api = Cov19API(filters=all_nations, structure=cases_and_deaths)

    data = api.get_json()
    df = api.get_dataframe()
    cumCases = []
    date = []
    newCases = []

    for case in data['data']:
            cumCases.append(case['cumCasesByPublishDate'])
            date.append(case['date'])
            newCases.append(case['newCasesByPublishDate'])

    return newCases, cumCases, date, df

if __name__ == '__main__':
    fig = go.Figure()
    area = ['Kingston Upon Thames','Cambridge','Manchester']
    for this_area in area:
        newCases, cumCases, date, df = get_nation_data(this_area)

        x = date
        y= newCases

        # fig.add_trace(px.line(df))
        fig.add_trace(go.Scatter(x=df['date'], y=df['newCasesByPublishDate'],
                                 mode='lines',
                                 name=this_area))


        # fig.add_trace(go.Scatter(x=date, y=newCases,
        #                          mode='lines',
        #                          name=this_area))
    fig.show()