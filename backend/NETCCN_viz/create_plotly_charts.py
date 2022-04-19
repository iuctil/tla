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
us_poverty= round((sum(demographics["E_POV"])/us_population)*100,1)
us_unemp= round((sum(demographics["E_UNEMP"])/us_population)*100,1)
us_age65= round((sum(demographics["E_AGE65"])/us_population)*100,1)
us_age17= round((sum(demographics["E_AGE17"])/us_population)*100,1)
us_disability= round((sum(demographics["E_DISABL"])/us_population)*100,1)
us_uninsured= round((sum(demographics["E_UNINSUR"])/us_population)*100,1)

utilizations = utilizations.sort_values(by="collection_week")
utilizations=utilizations.replace(-999999, 0) #replacing missing value 
utilizations['collection_week'] = pd.to_datetime(utilizations["collection_week"],format='%Y/%m/%d').dt.date

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
        print("creating demographics file for " + fipscode)
        county= demographics[demographics["FIPS"]==fipscode]
        county_population= county.iloc[0]["E_TOTPOP"]
        county_poverty=round((county.iloc[0]["E_POV"]/county_population),3)
        county_unemp= round((county.iloc[0]["E_UNEMP"]/county_population),3)
        county_age65= round((county.iloc[0]["E_AGE65"]/county_population),3)
        county_age17= round((county.iloc[0]["E_AGE17"]/county_population),3)
        county_disability=round((county.iloc[0]["E_DISABL"]/county_population),3)
        county_uninsured= round((county.iloc[0]["E_UNINSUR"]/county_population),3)
    
    #calculating metrics for state
        state=demographics[demographics["STATE"]==county.iloc[0]["STATE"]]
        state_population= sum(state["E_TOTPOP"])
        state_poverty= round((sum(state["E_POV"])/state_population),3)
        state_unemp= round((sum(state["E_UNEMP"])/state_population),3)
        state_age65= round((sum(state["E_AGE65"])/state_population),3)
        state_age17= round((sum(state["E_AGE17"])/state_population),3)
        state_disability= round((sum(state["E_DISABL"])/state_population),3)
        state_uninsured= round((sum(state["E_UNINSUR"])/state_population),3)

        cell_text = { 'countyName': county.iloc[0]["COUNTY"],
                    'State': county.iloc[0]["STATE"].lower().title(),
                'population': {'county': int(county_population), 'state':int(state_population),'us':int(us_population)},
               'belowPovertyPopulation': {'county': county_poverty, 'state':state_poverty,'us':us_poverty},
               'unemployedPopulation': {'county': county_unemp, 'state':state_unemp,'us':us_unemp},
               'uninsuredPopulation': {'county': county_uninsured, 'state':state_uninsured,'us':us_uninsured},
               'disabilityPopulation':{'county': county_disability, 'state':state_disability,'us':us_disability},
               '65OlderPopulation': {'county': county_age65, 'state':state_age65,'us':us_age65,},
               '17youngerPopulation': {'county': county_age17, 'state':state_age17,'us':us_age17}
        }

    

        # creating json file 
         # creating json file 
        json_string= json.dumps(cell_text, indent=4)
        with open("demographics/county."+fipscode+".json", 'w') as outfile:
            outfile.write(json_string)

def waterfall_charts():
    for index, row in NETCCN.iterrows():
        fipscode = str(row["site.fips"])
        provider_id= str(row['provider.num'])
        if (provider_id=='0'):
            continue
            
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
            continue
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
        
        plotly.io.write_json(fig, "waterfall/county."+fipscode+"hospital."+provider_id+".plotly.json", pretty=True)

covid_transmission_charts()
covid_cases_charts()
demographics_table()
waterfall_charts()
print("all done")
