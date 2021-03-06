import plotly.graph_objects as go
from src.toolbox.SignalProcessing import moving_average
from uk_covid19 import Cov19API
import math
from requests import get
from datetime import date

def get_region_data(area,second_wave_onward=True):

    # Can't get round request white space issue
    endpoint=('https://api.coronavirus.data.gov.uk/v2/data?' +
                'areaType=ltla&'
                'areaName=' + area + 
                '&metric=cumCasesByPublishDate&'
                'metric=newCasesByPublishDate')
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
    newCases = [x for x in newCases if x is not None] # filter out None

    return newCases, cumCases, date, df

def get_region_data_today(area):

    endpoint = 'https://api.coronavirus.data.gov.uk/v2/data'
    payload = {
        'areaType':'ltla',
        'areaName': area,
        'metric':['newCasesByPublishDate','cumCasesByPublishDate','cumDeathsByDeathDate']
    }
    response = get(endpoint, params=payload, timeout=10)

    if response.status_code >= 400:
        raise RuntimeError(f'Request failed: {response.text}')

    data = response.json()
    cumCases = data['body'][0]['cumCasesByPublishDate']
    death = data['body'][0]['cumDeathsByDeathDate']
    newCases = data['body'][0]['newCasesByPublishDate']
    date = data['body'][0]['date']

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
    newCases, cumCases, date, df = get_region_data('Kingston Upon Thames')
    # newCases, cumCases, date, df = get_region_data('Elmbridge')

    # get_region_data_today('Elmbridge')
    # print(newCases)
    from src.toolbox.SignalProcessing import moving_average

    fig = go.Figure()
    x = date
    y = newCases
    y_mva = moving_average(newCases, 7)

    fig.add_trace(go.Scatter(x=date, y=y_mva,
                                  mode='lines',
                                  name='a'))
    fig.update_layout(template="plotly_white",
                       title={
                           'text': "Surrey - Confirmed Daily Cases",
                           'x': 0.5,
                           'xanchor': 'center',
                           'yanchor': 'top'}
                       )
    fig.show()