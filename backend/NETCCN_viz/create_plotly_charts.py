#!/usr/bin/env python3
# coding: utf-8



#---------------Imports---------------#
import pandas as pd
import datetime as dt
#import chart_studio
import plotly.graph_objects as go
#import chart_studio.plotly as py
#from plotly.subplots import make_subplots
import plotly
import numpy as np
import json
#---------------Imports---------------#

#---------------Getting necessary files---------------#
print("loading cdc-covid-transmission..")
covid_cases= pd.read_csv("/mnt/scratch/datasources/cdc-covid-transmission/rows.csv", dtype={'fips_code':'object'})
# link to get data https://data.cdc.gov/Public-Health-Surveillance/United-States-COVID-19-County-Level-of-Community-T/nra9-vzzn

print("loading netccn central..")
NETCCN= pd.read_excel("/mnt/scratch/datasources/netccn/NETCCN_Central_active_complete.xlsx",dtype={'site.fips':'object'})

print("loading cdc SVI..")
svi=pd.read_csv("/mnt/scratch/datasources/cdc-svi/SVI2018_US_COUNTY.csv",dtype={'FIPS':'object'}) #link to data https://www.atsdr.cdc.gov/placeandhealth/svi/data_documentation_download.html


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


#new dataset with only columns of interest from SVI
demographics= svi[["STATE" ,"ST_ABBR", "COUNTY" ,"FIPS" ,"LOCATION" ,"AREA_SQMI","E_TOTPOP","E_POV", "E_UNEMP","E_AGE65","E_AGE17","E_DISABL","E_UNINSUR"]]
#calculating metrics for U.S (SVI)
us_population= sum(demographics["E_TOTPOP"])
us_poverty= round((sum(demographics["E_POV"])/us_population)*100,1)
us_unemp= round((sum(demographics["E_UNEMP"])/us_population)*100,1)
us_age65= round((sum(demographics["E_AGE65"])/us_population)*100,1)
us_age17= round((sum(demographics["E_AGE17"])/us_population)*100,1)
us_disability= round((sum(demographics["E_DISABL"])/us_population)*100,1)
us_uninsured= round((sum(demographics["E_UNINSUR"])/us_population)*100,1)


def covid_transmission_charts():
  print("creating covid_transmission_charts-----------------------")

  #  creating plotly charts
  for index, row in NETCCN.iterrows():
    fipscode = str(row["site.fips"])

    #there is an entry with fipscode set to 0 for some reason
    #TODO - we should clean this up when we load it
    if fipscode == "0":
      continue

    print("drawing plotly graph for " + fipscode)

    county_covid= covid_cases[covid_cases["fips_code"]==fipscode]
    county_covid_high=county_covid[county_covid["community_transmission_level"]=="high"]
    county_covid_substantial=county_covid[county_covid["community_transmission_level"]=="substantial"]
    county_covid_moderate=county_covid[county_covid["community_transmission_level"]=="moderate"]
    county_covid_low=county_covid[county_covid["community_transmission_level"]=="low"]


    fig = go.Figure()

    obj = go.Scatter(x = county_covid_high.date, y = county_covid_high.community_transmission_level, name="High",mode="markers",marker_color=county_covid_high.colors)

    obj1 = go.Scatter(x = county_covid_substantial.date, y = county_covid_substantial.community_transmission_level, name="Substantial",mode="markers",marker_color=county_covid_substantial.colors)

    obj2 = go.Scatter(x = county_covid_moderate.date, y = county_covid_moderate.community_transmission_level, name="Moderate",mode="markers",marker_color=county_covid_moderate.colors)

    obj3 = go.Scatter(x = county_covid_low.date, y = county_covid_low.community_transmission_level, name="Low",mode="markers", marker_color=county_covid_low.colors)

    fig.add_trace(obj3)
    fig.add_trace(obj2)
    fig.add_trace(obj1)
    fig.add_trace(obj)



    # Set title
    fig.update_layout(
    title_text=str (county_covid.iloc[0]["county_name"])+" Daily COVID-19 Community Transmission Level ")
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='COVID-19 Community Transmission Level')

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
    #with open('community_transmission_links.txt', 'a') as the_file:
    #    the_file.write(str(py.plot(fig1, filename = str(row["site.fips"])+"_transmission_level", auto_open=False))+'\n')
    plotly.io.write_json(fig, "covid-transmission/county."+fipscode+".plotly.json", pretty=True)

#creating plotly charts
def covid_cases_charts():
  print("creating covid covid cases chars-----------------------")

  for index, row in NETCCN.iterrows():
    fipscode = str(row["site.fips"])

    #there is an entry with fipscode set to 0 for some reason
    #TODO - we should clean this up when we load it
    if fipscode == "0":
      continue

    print("drawing plotly graph for " + fipscode)
    county_covid = covid_cases[covid_cases["fips_code"]==fipscode]
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
    plotly.io.write_json(fig, "covid-cases/county."+fipscode+".plotly.json", pretty=True)

#saving plotly links in file
#with open('covid_cases_links.txt', 'a') as the_file:
#  the_file.write(str(py.plot(fig, filename = str(row["site.fips"])+"_transmission_level", auto_open=False))+'\n')
def demographics_table():
    for index, row in NETCCN.iterrows():
        fipscode = str(row["site.fips"])
        if fipscode == "0":
            continue
    #calculating metrics for county
        county= demographics[demographics["FIPS"]==fipscode]
        county_population= county.iloc[0]["E_TOTPOP"]
        county_poverty=round((county.iloc[0]["E_POV"]/county_population)*100,1)
        county_unemp= round((county.iloc[0]["E_UNEMP"]/county_population)*100,1)
        county_age65= round((county.iloc[0]["E_AGE65"]/county_population)*100,1)
        county_age17= round((county.iloc[0]["E_AGE17"]/county_population)*100,1)
        county_disability=round((county.iloc[0]["E_DISABL"]/county_population)*100,1)
        county_uninsured= round((county.iloc[0]["E_UNINSUR"]/county_population)*100,1)
    
    #calculating metrics for state
        state=demographics[demographics["STATE"]==county.iloc[0]["STATE"]]
        state_population= sum(state["E_TOTPOP"])
        state_poverty= round((sum(state["E_POV"])/state_population)*100,1)
        state_unemp= round((sum(state["E_UNEMP"])/state_population)*100,1)
        state_age65= round((sum(state["E_AGE65"])/state_population)*100,1)
        state_age17= round((sum(state["E_AGE17"])/state_population)*100,1)
        state_disability= round((sum(state["E_DISABL"])/state_population)*100,1)
        state_uninsured= round((sum(state["E_UNINSUR"])/state_population)*100,1)

        cell_text = [["", county.iloc[0]["COUNTY"]+ " County", 'State: '+county.iloc[0]["STATE"].lower().title(), 'U.S.'],
        ["Population ", "{:,}".format(county_population), "{:,}".format(state_population), "{:,}".format(us_population)],
        [ "Percentage of Population below poverty",str(county_poverty)+'%', str(state_poverty)+'%', str(us_poverty)+'%'],
        [ "Percentage of Unemployed Population",str(county_unemp)+'%', str(state_unemp)+'%', str(us_unemp)+'%'],
        [  "Percentage of Uninsured Population ",str(county_uninsured)+'%', str(state_uninsured)+'%', str(us_uninsured)+'%'],
        [ "Percentage of Population with Disability",str(county_disability)+'%', str(state_disability)+'%', str(us_disability)+'%',],
        [ "Percentage of Population Aged 65 and older",str(county_age65)+'%', str(state_age65)+'%', str(us_age65)+'%'],
        [  "Percentage of Population Aged 17 and younger",str(county_age17)+'%', str(state_age17)+'%', str(us_age17)+'%']]

        # creating json file 
         # creating json file 
        json_string= json.dumps(cell_text, indent=4)
        with open("demographics/county."+fipscode+".json", 'w') as outfile:
            outfile.write(json_string)
covid_transmission_charts()
covid_cases_charts()
demographics_table()
print("all done")
