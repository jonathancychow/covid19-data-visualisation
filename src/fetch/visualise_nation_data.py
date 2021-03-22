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
        "newPeopleVaccinatedFirstDoseByPublishDate": "newPeopleVaccinatedFirstDoseByPublishDate"
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

    vaccinated = [x['newPeopleVaccinatedFirstDoseByPublishDate'] for x in data['data'] if x['newPeopleVaccinatedFirstDoseByPublishDate']]
    vaccinated_date=[x['date'] for x in data['data'] if x['newPeopleVaccinatedFirstDoseByPublishDate']]


    return newCases, cumCases, date, hospitalCases, newAdmission, vaccinated, vaccinated_date

def get_uk_data_latest():
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
        "cumPeopleVaccinatedFirstDoseByVaccinationDate": "cumPeopleVaccinatedFirstDoseByVaccinationDate"
    }

    api = Cov19API(filters=all_nations, structure=cases_and_deaths, latest_by='newCasesByPublishDate')
    data = api.get_json()
    cumCases = sum([value['cumCasesByPublishDate'] for value in data['data']])
    newCases = sum([value['newCasesByPublishDate'] for value in data['data']])
    date = data['data'][0]['date']

    return newCases, cumCases, date

def get_uk_vaccinated():
    all_nations = [
        "areaType=overview"
    ]
    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newPeopleVaccinatedFirstDoseByPublishDate":"newPeopleVaccinatedFirstDoseByPublishDate"
    }

    api = Cov19API(filters=all_nations, structure=cases_and_deaths)
    data = api.get_json()
    date = []
    vaccinated = []
    for this_date in data['data']:
        vaccinated.append(this_date['newPeopleVaccinatedFirstDoseByPublishDate'])
        date.append(this_date['date'])

    # cumCases = sum([value['cumCasesByPublishDate'] for value in data['data']])
    # newCases = sum([value['newCasesByPublishDate'] for value in data['data']])
    # date = data['data'][0]['date']

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
    print(get_nation_data('England'))
    # print(get_uk_vaccinated())