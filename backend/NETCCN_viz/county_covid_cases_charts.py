#!/usr/bin/env python
# coding: utf-8



#---------------Imports---------------#
import pandas as pd
import datetime as dt
import chart_studio
import plotly.graph_objects as go
import chart_studio.plotly as py
from plotly.subplots import make_subplots
import numpy as np
#---------------Imports---------------#


#---------------Getting necessary files---------------#
covid_cases= pd.read_csv("United_States_COVID-19_County_Level_of_Community_Transmission_Historical_Changes.csv", dtype={'fips_code':'object'})
# link to get data https://data.cdc.gov/Public-Health-Surveillance/United-States-COVID-19-County-Level-of-Community-T/nra9-vzzn
NETCCN= pd.read_excel("NETCCN_central_active_complete.xlsx",dtype={'site.fips':'object'})

#---------------Data cleaning and preparing---------------#
NETCCN["StatusLogStatusReceived_Start"]=pd.to_datetime(NETCCN["StatusLogStatusReceived_Start"],format='%Y/%m/%d').dt.date
NETCCN["actualStartDate"]=pd.to_datetime(NETCCN["actualStartDate"],format='%Y/%m/%d').dt.date
NETCCN["StatusLogStatusActive_Complete"]=pd.to_datetime(NETCCN["StatusLogStatusActive_Complete"],format='%Y/%m/%d').dt.date

covid_cases['date']=pd.to_datetime(covid_cases['date']).dt.date #changing the date format
covid_cases=covid_cases[covid_cases['date'] >= dt.date(2021, 1, 1)]
covid_cases= covid_cases[covid_cases['cases_per_100K_7_day_count_change'] != 'suppressed'] # delete rows with missing data
covid_cases["cases_per_100K_7_day_count_change"] = covid_cases["cases_per_100K_7_day_count_change"].replace({',':''}, regex=True) #changing the number of cases to numeric
covid_cases["cases_per_100K_7_day_count_change"] = pd.to_numeric(covid_cases["cases_per_100K_7_day_count_change"])
covid_cases = covid_cases.sort_values(by="date") #sorting by date

#plotly account credentials
username = 'mloukil1' # your username
api_key = 'bVYWAwlQx26iAIQFwCeH' # your api key - go to profile > settings > regenerate key
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

#creating plotly charts
for index, row in NETCCN.iterrows():
    county_covid= covid_cases[covid_cases["fips_code"]==str(row["site.fips"])]
    fig = go.Figure()
    fig.add_trace(
    go.Scatter(x=list(county_covid.date), y=list(county_covid.cases_per_100K_7_day_count_change)))

    # Set title
    fig.update_layout(
    title_text=str (county_covid.iloc[0]["county_name"])+" COVID-19 cases ")
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Number of COVID-19 cases per 100K')
    
# Add range slider
    fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)
#saving plotly links in file
    with open('covid_cases_links.txt', 'a') as the_file:
        the_file.write(str(py.plot(fig, filename = str(row["site.fips"])+"_transmission_level", auto_open=False))+'\n')
    
 