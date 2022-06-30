#!/usr/bin/env python3
# coding: utf-8

import pandas as pd
import datetime as dt
import plotly.graph_objects as go
import plotly
import numpy as np
import os
import json

print("loading cdc-covid-transmission..")
covid_cases= pd.read_csv("/mnt/scratch/datasources/cdc-covid-transmission/rows.csv", dtype={'fips_code':'object'})
# link to get data https://data.cdc.gov/Public-Health-Surveillance/United-States-COVID-19-County-Level-of-Community-T/nra9-vzzn

print("loading netccn central..")
NETCCN= pd.read_excel("/mnt/scratch/datasources/netccn/NETCCN_Central_active_complete.xlsx",dtype={'site.fips':'object'})

print("loading cdc SVI..")
svi=pd.read_csv("/mnt/scratch/datasources/cdc-svi/SVI2018_US_COUNTY.csv",dtype={'FIPS':'object'}) #link to data https://www.atsdr.cdc.gov/placeandhealth/svi/data_documentation_download.html

print ("loading hhs utilization")
utilizations= pd.read_csv("/mnt/scratch/datasources/healthdata.gov/utilizations.csv")

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
us_poverty= sum(demographics["E_POV"])/us_population
us_unemp= sum(demographics["E_UNEMP"])/us_population
us_age65= sum(demographics["E_AGE65"])/us_population
us_age17= sum(demographics["E_AGE17"])/us_population
us_disability= sum(demographics["E_DISABL"])/us_population
us_uninsured= sum(demographics["E_UNINSUR"])/us_population

utilizations = utilizations.sort_values(by="collection_week")
utilizations=utilizations.replace(-999999, 0) #replacing missing value
utilizations['collection_week'] = pd.to_datetime(utilizations["collection_week"],format='%Y/%m/%d').dt.date

def covid_transmission_charts(fipscode):
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
  return fig

#creating plotly charts
def covid_cases_charts(fips):
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
  return fig

#def demographics_table(fips):
#    county= demographics[demographics["FIPS"]==fipscode]
#    county_population= county.iloc[0]["E_TOTPOP"]
#    county_poverty=round((county.iloc[0]["E_POV"]/county_population),3)
#    county_unemp= round((county.iloc[0]["E_UNEMP"]/county_population),3)
#    county_age65= round((county.iloc[0]["E_AGE65"]/county_population),3)
#    county_age17= round((county.iloc[0]["E_AGE17"]/county_population),3)
#    county_disability=round((county.iloc[0]["E_DISABL"]/county_population),3)
#    county_uninsured= round((county.iloc[0]["E_UNINSUR"]/county_population),3)
#
#    #calculating metrics for state
#    state=demographics[demographics["STATE"]==county.iloc[0]["STATE"]]
#    state_population= sum(state["E_TOTPOP"])
#    state_poverty= round((sum(state["E_POV"])/state_population),3)
#    state_unemp= round((sum(state["E_UNEMP"])/state_population),3)
#    state_age65= round((sum(state["E_AGE65"])/state_population),3)
#    state_age17= round((sum(state["E_AGE17"])/state_population),3)
#    state_disability= round((sum(state["E_DISABL"])/state_population),3)
#    state_uninsured= round((sum(state["E_UNINSUR"])/state_population),3)
#
#    return { 'countyName': county.iloc[0]["COUNTY"],
#                'state': county.iloc[0]["STATE"].lower().title(),
#            'population': {'county': int(county_population), 'state':int(state_population),'us':int(us_population)},
#           'belowPovertyPopulation': {'county': county_poverty, 'state':state_poverty,'us':us_poverty},
#           'unemployedPopulation': {'county': county_unemp, 'state':state_unemp,'us':us_unemp},
#           'uninsuredPopulation': {'county': county_uninsured, 'state':state_uninsured,'us':us_uninsured},
#           'disabilityPopulation':{'county': county_disability, 'state':state_disability,'us':us_disability},
#           '65OlderPopulation': {'county': county_age65, 'state':state_age65,'us':us_age65,},
#           '17youngerPopulation': {'county': county_age17, 'state':state_age17,'us':us_age17}
#    }

def waterfall_charts(fips, provider_id):
  if ('NaT' in str(row["StatusLogStatusActive_Complete"])):
    waterfall_start= row["StatusLogStatusReceived_Start"]-dt.timedelta(weeks = 2)
    waterfall_end= row["actualStartDate"]+dt.timedelta(days = 9)
    request_date=row["StatusLogStatusReceived_Start"]
    start_date=row["actualStartDate"]
  else:
    waterfall_start= row["StatusLogStatusReceived_Start"]-dt.timedelta(weeks = 2)
    waterfall_end= row["StatusLogStatusActive_Complete"]+dt.timedelta(days = 9)
    request_date=row["StatusLogStatusReceived_Start"]
    start_date=row["actualStartDate"]
    end_date=row["StatusLogStatusActive_Complete"]

  ## Creating dataframe for specific hospital
  Specific_Hospital= utilizations[utilizations['hospital_pk']==provider_id]
  if (Specific_Hospital.shape[0]==0):
    return None

  Specific_Hospital=Specific_Hospital[(Specific_Hospital['collection_week'] >= waterfall_start) &
                                  (Specific_Hospital['collection_week'] <= waterfall_end)]
  Specific_Hospital_filtered= Specific_Hospital[["collection_week"]]
  Specific_Hospital_filtered["inpatient_beds_used_covid_7_day_avg"]= Specific_Hospital["inpatient_beds_used_covid_7_day_sum"]/7
  Specific_Hospital_filtered["staffed_icu_adult_patients_confirmed_covid_7_day_avg"]= Specific_Hospital["staffed_icu_adult_patients_confirmed_covid_7_day_sum"]/7
  Specific_Hospital_filtered["total_covid_patients"]= Specific_Hospital_filtered["inpatient_beds_used_covid_7_day_avg"]+Specific_Hospital_filtered["staffed_icu_adult_patients_confirmed_covid_7_day_avg"]

  Specific_Hospital_filtered= Specific_Hospital_filtered.set_index("collection_week")
  deltas = [Specific_Hospital_filtered['total_covid_patients'][i] if
      i==0 else Specific_Hospital_filtered['total_covid_patients'][i]-Specific_Hospital_filtered['total_covid_patients'][i-1]
      for i in range(len(Specific_Hospital_filtered))]
  Specific_Hospital_filtered['delta'] = np.round(deltas,1)
  Specific_Hospital_filtered=Specific_Hospital_filtered.reset_index()
  Specific_Hospital_filtered["measure"]= "relative"
  Specific_Hospital_filtered.iloc[-1,Specific_Hospital_filtered.columns.get_loc('measure')] = "total"
  Specific_Hospital_filtered.iloc[-1,Specific_Hospital_filtered.columns.get_loc('delta')] = np.round(Specific_Hospital_filtered.iloc[-1,Specific_Hospital_filtered.columns.get_loc('total_covid_patients')],1)

  fig = go.Figure(go.Waterfall(
    orientation = "v",
    measure = Specific_Hospital_filtered.measure,
    x = Specific_Hospital_filtered.collection_week,
    textposition = "inside",
    text = Specific_Hospital_filtered.delta,
    y = Specific_Hospital_filtered.delta,
    connector = {"line":{"color":"rgb(63, 63, 63)"}},
  ))

  #fig.update_xaxes(range=[-1, max(Specific_Hospital_filtered["total_covid_patients"])*1.05])
  if ('NaT' in str(row["StatusLogStatusActive_Complete"])):
    fig.add_trace(go.Scatter(
    x=[request_date,start_date],
    y=[-0.5, -0.5],
    text=["<b>Request</b>",
    "<b>Deployment <br> Start</b>"],
    mode="text",
    textposition="middle center",
    textfont=dict(
    size=12,
    color="black"
    )))
  else:
    fig.add_trace(go.Scatter(
    x=[request_date,start_date,end_date],
    y=[-0.5, -0.5,-0.5],
    text=["<b>Request</b>",
    "<b>Deployment <br> Start</b>","<b>Deployment <br> End</b>" ],
    mode="text",
    textposition="middle center",
    textfont=dict(
    size=12,
    color="black"
    )))

  # Add shapes
  fig.update_shapes(dict(xref='x', yref='y'))
  fig.update_layout(
    title = 'Number of COVID-19 patients in '+ Specific_Hospital.iloc[0]["hospital_name"].lower().title()+'<br> (weekly average) (inpatient beds + Staffed ICU beds)',
    title_x=0.5,
    yaxis_range=[-2, max(Specific_Hospital_filtered["total_covid_patients"])*1.05],
    xaxis_title='Date',
    yaxis_title="'Average number of COVID-19 patients'",
    showlegend = False
  )

  return fig

#we need a list of NETCCN hospital charts before we can construct the county page
netccn_md = {}
for index, row in NETCCN.iterrows():
  fipscode = str(row["site.fips"])

  #there is an entry with fipscode set to 0 for some reason
  if fipscode == "0":
    continue

  #place to store the plotly graphs
  jsonPath = "../static/netccn/"+fipscode
  if not os.path.exists(jsonPath):
    os.makedirs(jsonPath)

  provider_id = str(row['provider.num'])
  if provider_id !='0':
    print("creating waterfall chart for "+provider_id)
    fig = waterfall_charts(fipscode, provider_id)
    if fig:
      plotly.io.write_json(fig, jsonPath+"/hospital."+provider_id+".plotly.json", pretty=True)
      if not fipscode in netccn_md:
        netccn_md[fipscode] = ""

      netccn_md[fipscode] += f"{{{{<plotly json=\"netccn/{fipscode}/hospital.{provider_id}.plotly.json\" height=\"400px\">}}}}\n"

#then create county level page
for index, row in NETCCN.iterrows():
  fipscode = str(row["site.fips"])

  #there is an entry with fipscode set to 0 for some reason
  if fipscode == "0":
    continue

  print("processing", row["site.fips"])

  mdPath = "../content/netccn/"+fipscode
  if not os.path.exists(mdPath):
    os.makedirs(mdPath)

  county= demographics[demographics["FIPS"]==fipscode]
  county_population= int(county.iloc[0]["E_TOTPOP"])
  county_poverty= county.iloc[0]["E_POV"]/county_population
  county_unemp= county.iloc[0]["E_UNEMP"]/county_population
  county_age65= county.iloc[0]["E_AGE65"]/county_population
  county_age17= county.iloc[0]["E_AGE17"]/county_population
  county_disability= county.iloc[0]["E_DISABL"]/county_population
  county_uninsured= county.iloc[0]["E_UNINSUR"]/county_population

  #calculating metrics for state
  state=demographics[demographics["STATE"]==county.iloc[0]["STATE"]]
  state_population= sum(state["E_TOTPOP"])
  state_poverty= sum(state["E_POV"])/state_population
  state_unemp= sum(state["E_UNEMP"])/state_population
  state_age65= sum(state["E_AGE65"])/state_population
  state_age17= sum(state["E_AGE17"])/state_population
  state_disability= sum(state["E_DISABL"])/state_population
  state_uninsured= sum(state["E_UNINSUR"])/state_population

  countyName = county.iloc[0]["COUNTY"]
  stateName = county.iloc[0]["STATE"].lower().title()

  def f(v):
    return '{:,}'.format(v)
  def fp(v):
    return '{:0.0%}'.format(v)

  md = f"""
---
title: "NETCCN deployment information for {countyName} County (fips:{fipscode})"
description: "NETCCN deployment"
weight: 100
toc: false
plotly: true
---

For this county, population demographic data is compared to state and national values.

| | {countyName} County | {stateName} | U.S. |
| ----------- | ----------- | ----------- | -------- |
| Population | {f(county_population)} | {f(state_population)} | {f(us_population)} |
| Percentage of Population below poverty | {fp(county_poverty)} | {fp(state_poverty)} | {fp(us_poverty)} |
| Percentage of Unemployed Population | {fp(county_unemp)} | {fp(state_unemp)} | {fp(us_unemp)} |
| Percentage of Uninsured Population | {fp(county_uninsured)} | {fp(state_uninsured)} | {fp(us_uninsured)} |
| Percentage of Population with Disability | {fp(county_disability)} | {fp(state_disability)} | {fp(us_disability)} |
| Percentage of Population Aged 65 and older | {fp(county_age65 )} | {fp(state_age65 )} | {fp(us_age65)} |
| Percentage of Population Aged 17 and younger | {fp(county_age17 )} | {fp(state_age17 )} | {fp(us_age17)} |

  """

  print("drawing plotly graph for " + fipscode)

  fig = covid_transmission_charts(fipscode)
  plotly.io.write_json(fig, jsonPath+"/covid_transmission.plotly.json", pretty=True)
  md += """

For this county, COVID-19 community transmission levels are depicted as part of understanding demand for critical care requirements in the region.

"""
  md += f"{{{{<plotly json=\"netccn/{fipscode}/covid_transmission.plotly.json\" height=\"400px\">}}}}\n"

  fig = covid_cases_charts(fipscode)
  plotly.io.write_json(fig, jsonPath+"/covid_cases.plotly.json", pretty=True)
  md += """

TODO - describe covid cases plot below

  """
  md += f"{{{{<plotly json=\"netccn/{fipscode}/covid_cases.plotly.json\" height=\"400px\">}}}}\n"

  #with open(path+"/demographics.json", 'w') as outfile:
  #    outfile.write(json_string)

  if fipscode in netccn_md:
    md += """

For the following hospitals, average number of COVID-19 patients at a start date, with weekly changes shown in a waterfall chart, with increases depicted in green and decreases in red.  Total COVID-19 patients at the end of the selected period range is depicted in blue.  The following NETCCN deployment dates are noted as available, "week of the request", "week of the start of the deployment".  Purpose of graph is understanding the critical care conditions at the point in time when hospitals requested support and the length of time before the deployment started, including the change in conditions over the period.

"""
    md += netccn_md[fipscode]

  with open(mdPath+"/_index.md", "w") as mdf:
      mdf.write(md)

print("all done")


