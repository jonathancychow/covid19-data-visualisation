import plotly.graph_objects as go
from src.toolbox.SignalProcessing import moving_average
from uk_covid19 import Cov19API
import math
from requests import get
from datetime import date

def get_region_data(area,second_wave_onward=True):

    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        # "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        # "cumCasesByPublishDate": "cumCasesByPublishDate",
        # "newDeathsByDeathDate": "newDeathsByDeathDate",
        # "cumDeathsByDeathDate": "cumDeathsByDeathDate",
        # "cumPeopleVaccinatedFirstDoseByVaccinationDate":"cumPeopleVaccinatedFirstDoseByVaccinationDate"
    }


    endpoint = ('https://api.coronavirus.data.gov.uk/v2/data?' + 
                'areaType=ltla&'+
                'areaName=' + area + 
                '&metric=newCasesByPublishDate&' +
                'metric=cumCasesByPublishDate' + 
                # 'metric=cumCasesByPublishDate' + 
                # 'metric=cumCasesByPublishDate' + 
                # 'metric=cumCasesByPublishDate' + 
                '&format=json')

    # endpoint = (
    #     'https://api.covid19api.com/dayone/country/' + country + '/status/'+ status +'/live'
    # )
    response = get(endpoint, timeout=10)

    if response.status_code >= 400:
        raise RuntimeError(f'Request failed: {response.text}')

    data = response.json()

    if second_wave_onward:
        discard_after_date = '2020-08-11' 
    else:
        discard_after_date = str(date.today())


    cumCases = None
    df = None
    date = [x['date'] for x in data['body'] if x['date'] > discard_after_date]
    newCases = [x['newCasesByPublishDate'] for x in data['body'] if x['date'] > discard_after_date]

    return newCases, cumCases, date, df

def get_region_data_today(area):
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
    cumCases = data['data'][0]['cumCasesByPublishDate']
    death = data['data'][0]['cumDeathsByDeathDate']
    newCases = data['data'][0]['newCasesByPublishDate']
    date = data['data'][0]['date']

    return newCases, cumCases, death, date

if __name__ == '__main__':
    # fig = go.Figure()
    # fig.update_layout(
    #     title={
    #         'text': "Covid Cases - 7days averaged",
    #         'xanchor': 'center'
    #         })
    # area = ['Kingston Upon Thames','Richmond Upon Thames','Epsom and Ewell','Hackney and City of London']
    # # area = ['Manchester', 'Liverpool']
    #
    # for this_area in area:
    #     newCases, cumCases, date, df = get_region_data(this_area)
    #
    #     x = date
    #     y = newCases
    #     N = 7
    #     y_mva = moving_average(df['newCasesByPublishDate'], N)
    #
    #     # fig.add_trace(go.Scatter(x=df['date'], y=df['newCasesByPublishDate'],
    #     #                          mode='lines',
    #     #                          name=this_area))
    #
    #     fig.add_trace(go.Scatter(x=df['date'][(math.ceil(N/2)):], y=y_mva,
    #                              mode='lines',
    #                              name=this_area))
    #
    # fig.show()
    # newCases, cumCases, date, df = get_region_data('Elmbridge')
    get_region_data_today('Elmbridge')
    print(newCases)
