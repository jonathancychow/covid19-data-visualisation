from requests import get
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.toolbox.SignalProcessing import moving_average

def get_country_data(country, status):
    endpoint = (
        'https://api.covid19api.com/dayone/country/' + country + '/status/'+ status +'/live'
    )
    response = get(endpoint, verify=False, timeout=10)

    if response.status_code >= 400:
        raise RuntimeError(f'Request failed: {response.text}')

    allData = response.json()

    cumulativeCase = []
    dailyCase=[]
    date = []
    for dayData in allData:
        if not dayData['Province']:
            cumulativeCase.append(dayData['Cases'])
            date.append(dayData['Date'])
            if not dailyCase:
                dailyCase.append(dayData['Cases'])
            else:
                dailyCase.append(cumulativeCase[-1]-cumulativeCase[-2])

    return date, cumulativeCase, dailyCase


if __name__ == '__main__':

    country = ['united-kingdom','spain', 'france','germany']
    status='confirmed'
    fig = make_subplots(rows=2, cols=1,subplot_titles=('Confirmed Cases','Deaths'))

    for thisCountry in country:
        date, cumulativeCase, dailyCase = get_country_data(thisCountry, status)

        x = date
        y= dailyCase
        N = 7
        y_mva = moving_average(dailyCase, N)

        fig.add_trace(go.Scatter(x=date,y=y_mva,
                                 mode='lines',
                                 name=thisCountry),
                                 row=1, col=1)

    status = 'deaths'
    for thisCountry in country:
        date, cumulativeCase, dailyCase = get_country_data(thisCountry, status)

        x = date
        y= dailyCase
        y_mva = moving_average(dailyCase, N)

        fig.add_trace(go.Scatter(x=date,y=y_mva,
                                 mode='lines',
                                 name=thisCountry),
                                 row=2, col=1)

    fig.show()
