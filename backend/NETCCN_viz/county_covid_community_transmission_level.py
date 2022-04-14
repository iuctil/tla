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

conditions = [
    (covid_cases['community_transmission_level'] == "high"),
    (covid_cases['community_transmission_level'] == "substantial") ,
    (covid_cases['community_transmission_level'] == "moderate") ,
    (covid_cases['community_transmission_level'] =="low" )
    ]

# create a list of the values we want to assign for each condition
values = ['tomato', 'orange', 'gold', 'mediumseagreen']

# create a new column and use np.select to assign values to it using our lists as arguments
covid_cases['colors'] = np.select(conditions, values)




#plotly credentials
username = 'mloukil1' # your username
api_key = 'bVYWAwlQx26iAIQFwCeH' # your api key - go to profile > settings > regenerate key
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

 #  creating plotly charts
for index, row in NETCCN.iterrows():
    county_covid= covid_cases[covid_cases["fips_code"]==str(row["site.fips"])]
    county_covid_high=county_covid[county_covid["community_transmission_level"]=="high"]
    county_covid_substantial=county_covid[county_covid["community_transmission_level"]=="substantial"]
    county_covid_moderate=county_covid[county_covid["community_transmission_level"]=="moderate"]
    county_covid_low=county_covid[county_covid["community_transmission_level"]=="low"]
    
    
    fig1 = go.Figure()
    
    obj = go.Scatter(x = county_covid_high.date, y = county_covid_high.community_transmission_level, name="High",mode="markers",marker_color=county_covid_high.colors)

    obj1 = go.Scatter(x = county_covid_substantial.date, y = county_covid_substantial.community_transmission_level, name="Substantial",mode="markers",marker_color=county_covid_substantial.colors)

    obj2 = go.Scatter(x = county_covid_moderate.date, y = county_covid_moderate.community_transmission_level, name="Moderate",mode="markers",marker_color=county_covid_moderate.colors)

    obj3 = go.Scatter(x = county_covid_low.date, y = county_covid_low.community_transmission_level, name="Low",mode="markers", marker_color=county_covid_low.colors)

    fig1.add_trace(obj3)
    fig1.add_trace(obj2)
    fig1.add_trace(obj1)
    fig1.add_trace(obj)
    
    
    
    # Set title
    fig1.update_layout(
    title_text=str (county_covid.iloc[0]["county_name"])+" Daily COVID-19 Community Transmission Level ")
    fig1.update_xaxes(title_text='Date')
    fig1.update_yaxes(title_text='COVID-19 Community Transmission Level')
    
# Add range slider
    fig1.update_layout(
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
    with open('community_transmission_links.txt', 'a') as the_file:
        the_file.write(str(py.plot(fig1, filename = str(row["site.fips"])+"_transmission_level", auto_open=False))+'\n')

    
