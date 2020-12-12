import pandas as pd
from pathlib import Path

def population(borough):

    excel_name = 'ukmidyearestimates20192020ladcodes.xls'
    data = pd.read_excel(open(excel_name, 'rb'),sheet_name='MYE3',index_col=1, header=4, usecols='A:D')
    data = data.transpose()

    # df = pd.DataFrame(data)
    # data['Name'][0]
    # data['Estimated Population  mid-2018'][0]
    return data[borough]['Estimated Population  mid-2018']

def get_population_df():
    excel_name = Path("fetch/ukmidyearestimates20192020ladcodes.xls")
    # excel_name = 'ukmidyearestimates20192020ladcodes.xls'
    #  = '../fetch/ukmidyearestimates20192020ladcodes.xls'

    data = pd.read_excel(open(excel_name, 'rb'),sheet_name='MYE3',index_col=1, header=4, usecols='A:D')
    data = data.transpose()

    # df = pd.DataFrame(data)
    # data['Name'][0]
    # data['Estimated Population  mid-2018'][0]
    return data

def case_density_conversion(input, borough):
    df= get_population_df()
    population = df[borough]['Estimated Population  mid-2018']
    # [x / myInt for x in myList]
    # print(population)
    # print(input)
    output=[]
    for this_value in input:
        if this_value == None:
            output.append(None)
        else:
            output.append(this_value/population)
    return output

if __name__ == '__main__':
    # borough = 'Kingston upon Thames'
    borough = 'England'
    print(population(borough))
    df = get_population_df()
    print(df[borough]['Estimated Population  mid-2018'])