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
        "newAdmissions": "newAdmissions",
        "newPeopleVaccinatedFirstDoseByPublishDate": "newPeopleVaccinatedFirstDoseByPublishDate",
        "newPeopleVaccinatedSecondDoseByPublishDate": "newPeopleVaccinatedSecondDoseByPublishDate"
    }
    nation_filter = [
        'areaType=nation',
        'areaName=' + nation
    ]
    api = Cov19API(filters=nation_filter, structure=cases_and_deaths)

    data = api.get_json()
    cumCases = [x['cumCasesByPublishDate'] for x in data['data']]
    date = [x['date'] for x in data['data']]
    newCases = [x['newCasesByPublishDate'] for x in data['data']]
    hospitalCases = [x['hospitalCases'] for x in data['data']]
    newAdmission = [x['newAdmissions'] for x in data['data']]
    first_dose = [x['newPeopleVaccinatedFirstDoseByPublishDate'] for x in data['data'] if x['newPeopleVaccinatedFirstDoseByPublishDate']]
    second_dose = [x['newPeopleVaccinatedSecondDoseByPublishDate'] for x in data['data'] if x['newPeopleVaccinatedSecondDoseByPublishDate']]
    vaccinated_date=[x['date'] for x in data['data'] if x['newPeopleVaccinatedFirstDoseByPublishDate']]
    vaccinated = [sum(x) for x in zip(first_dose, second_dose)]

    return newCases, cumCases, date, hospitalCases, newAdmission, vaccinated, vaccinated_date

def get_uk_data_latest():
    endpoint = 'https://api.coronavirus.data.gov.uk/v2/data'
    payload = {
        'areaType':'overview',
        'metric':['newCasesByPublishDate','cumCasesByPublishDate']
    }
    response = get(endpoint, params=payload, timeout=10)

    if response.status_code >= 400:
        raise RuntimeError(f'Request failed: {response.text}')

    data = response.json()

    cumCases = data['body'][0]['cumCasesByPublishDate']
    newCases = data['body'][0]['newCasesByPublishDate']
    date = data['body'][0]['date']

    return newCases, cumCases, date

def get_uk_vaccinated():
    endpoint = 'https://api.coronavirus.data.gov.uk/v2/data'
    payload = {
        'areaType':'overview',
        'metric':['newPeopleVaccinatedFirstDoseByPublishDate', 'newPeopleVaccinatedSecondDoseByPublishDate']
    }
    response = get(endpoint, params=payload, timeout=10)

    if response.status_code >= 400:
        raise RuntimeError(f'Request failed: {response.text}')

    data = response.json()
    
    date = [x['date'] for x in data['body']]
    first_dose = [x['newPeopleVaccinatedFirstDoseByPublishDate'] for x in data['body']]
    second_dose = [x['newPeopleVaccinatedSecondDoseByPublishDate'] for x in data['body']]
    vaccinated = [sum(x) for x in zip(first_dose, second_dose)]

    return vaccinated, date

if __name__ == '__main__':
    # fig = go.Figure()
    # fig = make_subplots(rows=3, cols=1,subplot_titles=('Confirmed Cases','Hospital Cases', 'New Admission'))
    #
    # nations = ['England','Wales','Scotland','Northern Ireland']
    # for this_nation in nations:
    #     newCases, cumCases, date, hospitalCases, newAdmission = get_nation_data(this_nation)
    #
    #     x = date
    #     y = newCases
    #
    #     fig.add_trace(go.Scatter(x=x, y=y,
    #                              mode='lines',
    #                              name=this_nation),
    #                              row=1,
    #                              col=1
    #                   )
    #     y = hospitalCases
    #     fig.add_trace(go.Scatter(x=x, y=y,
    #                              mode='lines',
    #                              name=this_nation),
    #                              row=2,
    #                              col=1
    #                   )
    #     y = newAdmission
    #     fig.add_trace(go.Scatter(x=x, y=y,
    #                              mode='lines',
    #                              name=this_nation),
    #                   row=3,
    #                   col=1
    #                   )
    #
    # fig.show()
    # print(get_uk_data_latest())
    # print(get_nation_data('Northern Ireland'))
    print(get_uk_vaccinated())