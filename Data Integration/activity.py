import pandas as pd
import numpy as np
import datetime as dt

def transform_acs(filename):
    # One row per county
    # Columns: Name, State, Population, Poverty, PerCapitaIncome, ID
    df = pd.read_csv(filename, usecols = ['TractId', 'State', 'County', 'TotalPop', 'IncomePerCap', 'Poverty'])
    df.columns = ['ID', 'State', 'County', 'Population', 'PerCapitaIncome', 'Poverty']    

    # Apply a "weight" to poverty and per capita percents, based off population
    df['weighted_pov'] = df['Population'] * df['Poverty']
    df['weighted_inc'] = df['Population'] * df['PerCapitaIncome']

    df1 = df.groupby(['County', 'State']).agg({'ID':'first', 'Population':sum, 'weighted_pov':sum, 'weighted_inc':sum}).reset_index()

    df1['Poverty'] = (df1['weighted_pov'] / df1['Population']).round(2)
    del df1['weighted_pov']

    df1['PerCapitaIncome'] = (df1['weighted_inc'] / df1['Population']).round(2)
    del df1['weighted_inc']

    #print(df1.head(20))
    return df1

def transform_covid(filename):
    # Data about COVID cases and deaths for each USA county
    # Desired Columns: ID, Month, Cases, Deaths
    # Current Columns: date, county, state, fips, cases, deaths

    df = pd.read_csv(filename)
    df['month'] = pd.to_datetime(df['date']).dt.month
    df['year'] = pd.to_datetime(df['date']).dt.year

    df1 = df.groupby(['county', 'state', 'month', 'year']).agg({'cases':sum, 'deaths':sum}).reset_index()

    df1.columns = ['County', 'State', 'Month', 'Year', 'Cases', 'Deaths']

    res = df1[df1['County'] == 'Malheur']
    print(res)
    return df1

def integrate(county_info, COVID_monthly):
    # One row per county
    # Columns: ID, Population, PerCapitaIncome, TotalCases, TotalDeaths, TotalCasesPer100K, TotalDeathsPer100K

    df = pd.concat([county_info, COVID_monthly], axis=1, join='outer')
    df = df.loc[:, ~df.columns.duplicated()]

    #df1 = df.groupby(['ID', 'County', 'State', 'Population', 'Poverty', 'PerCapitaIncome']).agg({'Cases':sum, 'Deaths':sum}).reset_index()

    df['TotalCasesPer100K'] = (df['Cases'] / (df['Population'] / 100000)).round(2)
    df['TotalDeathsPer100K'] = (df['Deaths'] / (df['Population'] / 100000)).round(2)
    
    #res = df[df['County'] == 'Harlan County']
    #print(res.head(50))

    return df

county_info = transform_acs("acs2017_census_tract_data.csv")
COVID_monthly = transform_covid("COVID_county_data.csv")
COVID_summary = integrate(county_info, COVID_monthly)

# Calculate Pearson correlation coefficient R for pairs of columns.
# Ex: R = df['TotalCasesPer100K'].corr(df['Poverty'])

# TODO: Compute the correlation coefficient for the following relationships for all Oregon counties

# COVID total cases vs. % population in poverty

#R = COVID_summary['Cases'].corr(COVID_summary['Poverty'])
# COVID total deaths vs. % population in poverty
#R = COVID_summary['Deaths'].corr(COVID_summary['Poverty'])
# COVID total cases vs. Per Capita Income level
#R = COVID_summary['Cases'].corr(COVID_summary['PerCapitaIncome'])
# COVID total deaths vs. Per Capita Income level
#R = COVID_summary['Deaths'].corr(COVID_summary['PerCapitaIncome'])


# Across all of the counties in the entire USA:

# COVID total cases vs. % population in poverty
R = COVID_summary['Cases'].corr(COVID_summary['Poverty'])
#print(R)

# COVID total deaths vs. % population in poverty
R = COVID_summary['Deaths'].corr(COVID_summary['Poverty'])
#print(R)

# COVID total cases vs. Per Capita Income level
R = COVID_summary['Cases'].corr(COVID_summary['PerCapitaIncome'])
#print(R)

# COVID total deaths vs. Per Capita Income level
R = COVID_summary['Deaths'].corr(COVID_summary['PerCapitaIncome'])
#print(R)

# For all counties: 
# Correlation between population and COVID cases
R = COVID_summary['Cases'].corr(COVID_summary['Population'])
#print(R)

# Correlation between population and COVID deaths
R = COVID_summary['Deaths'].corr(COVID_summary['Population'])
#print(R)