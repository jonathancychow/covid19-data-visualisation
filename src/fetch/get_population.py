import pandas as pd
from pathlib import Path
import math

def population(borough):

    excel_name = 'ukmidyearestimates20192020ladcodes.xls'
    data = pd.read_excel(open(excel_name, 'rb'),sheet_name='MYE3',index_col=1, header=4, usecols='A:D')
    data = data.transpose()

    return data[borough]['Estimated Population  mid-2018']

def get_borough_population_df():
    current_file_dir = Path(__file__).resolve()
    current_dir = current_file_dir.parent
    excel_path = Path(current_dir,'ukmidyearestimates20192020ladcodes.xls')
    excel_name = excel_path

    data = pd.read_excel(open(excel_name, 'rb'),sheet_name='MYE3',index_col=1, header=4, usecols='A:D')
    data = data.transpose()

    return data

def get_countries_population_df():
    data = {'United-Kingdom': 66460344,
            'Spain': 46796540,
            'France': 66977107,
            'Germany': 82905782,
            'Italy': 60421760,
            'Belgium': 11433256,
            'Switzerland':8513227,
            'Luxembourg':607950,
            'Denmark':5793636,
            'Sweden':10175214,
            'Norway':5311916,
            'Poland':37974750,
            'Ukraine':44622516,
            'Belarus':9483499,
            'United States': 326687501
            }





    return data

def case_density_conversion(input, borough, df):
    population = df[borough]['Estimated Population  mid-2018']

    if type(input) == int:
        output = math.floor(100000 * input / population)
    else:
        # input is list
        output=[]
        for this_value in input:
            if this_value == None:
                output.append(None)
            else:
                output.append(100000 * this_value/population)
    return output

if __name__ == '__main__':
    # borough = 'Kingston upon Thames'
    # borough = 'ENGLAND'
    # print(population(borough))
    # df = get_population_df()
    # print(df[borough]['Estimated Population  mid-2018'])
    a = get_countries_population_df()
    print(a['Italy'])