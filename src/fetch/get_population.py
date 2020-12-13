import pandas as pd
from pathlib import Path
import math

def population(borough):

    excel_name = 'ukmidyearestimates20192020ladcodes.xls'
    data = pd.read_excel(open(excel_name, 'rb'),sheet_name='MYE3',index_col=1, header=4, usecols='A:D')
    data = data.transpose()

    return data[borough]['Estimated Population  mid-2018']

def get_population_df():
    current_file_dir = Path(__file__).resolve()
    current_dir = current_file_dir.parent
    excel_path = Path(current_dir,'ukmidyearestimates20192020ladcodes.xls')
    excel_name = excel_path

    data = pd.read_excel(open(excel_name, 'rb'),sheet_name='MYE3',index_col=1, header=4, usecols='A:D')
    data = data.transpose()

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
    borough = 'ENGLAND'
    # print(population(borough))
    df = get_population_df()
    print(df[borough]['Estimated Population  mid-2018'])