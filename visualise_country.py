from requests import get
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def get_country_data(country, status):
    endpoint = (
        'https://api.covid19api.com/dayone/country/' + country + '/status/'+ status +'/live'
    )

    response = get(endpoint, timeout=10)

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

        fig.add_trace(go.Scatter(x=date,y=dailyCase,
                                 mode='lines',
                                 name=thisCountry),
                                 row=1, col=1)

    status = 'deaths'
    for thisCountry in country:
        date, cumulativeCase, dailyCase = get_country_data(thisCountry, status)

        x = date
        y= dailyCase

        fig.add_trace(go.Scatter(x=date,y=dailyCase,
                                 mode='lines',
                                 name=thisCountry),
                                 row=2, col=1)

    fig.show()
