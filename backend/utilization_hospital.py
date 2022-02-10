#!/usr/bin/env python3
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

#mariem should change this to somewhere else for local testing
basedir="/mnt/scratch/datasources/healthdata.gov"

print("loading utilization.csv")
df=pd.read_csv(basedir+"/utilizations.1000.csv", header=0,index_col=False)

df = df.sort_values(by="collection_week") #sorting dataset by year

hospitals_ids = df['hospital_pk'].unique() #[0:4]# getting the unique hospital_pk

df=df.replace(-999999, -7) #replacing missing value

#print(df.head())
#sys.exit(1)

# Parent Directory path
content_dir = "../content/hospitals"

for id in hospitals_ids:
    print("handling hospital", id)

    md="""---
title: "hospital information for $hospital_id
description: "....."
lead: "...."
date: 2021-08-10T15:22:20+01:00
lastmod: 2021-08-10T15:22:20+01:00
draft: false
#menu:
#  bplp:
#    parent: "articles"
#weight: 450
toc: true
---
"""

    df_slice= df[df['hospital_pk']== id] #dataframe for each hospital
    path = os.path.join(content_dir, str(id))
    if not os.path.exists(path):
      os.mkdir(path) #creating a directory for each hospital
    df_slice.to_csv(path+ "/utilization.csv",index=False) # saving each hospital data

for id in hospitals_ids:
    hospital_id = str(id)
    path = os.path.join(content_dir, hospital_id)
    df_slice=pd.read_csv(path+ "/"+hostpital_id+"_utilization.csv")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_slice["collection_week"], y=df_slice["inpatient_beds_used_covid_7_day_sum"]/7,
                   mode='lines',
                   name='average inpatient beds used for COVID-19'))
    fig.add_trace(go.Scatter(x=df_slice["collection_week"], y=df_slice["staffed_icu_adult_patients_confirmed_covid_7_day_sum"]/7,
                   mode='lines',
                   name='average ICU beds used for COVID-19'))
    fig.write_image(path+ "/utilization_COVID19.png")
    #fig.write_html(path+ "/"+str(id)+"_utilization_COVID19.html")
    #fig.write_json(path+ "/"+str(id)+"_utilization_COVID19.json")


    if True:
      md+="""
This hospital is doomed. don't visit.
"""

   if True:
      md+="""
here is the current hostpital utilization
![figure1](../utilization_COVID19.png)"
"""

    with open(path+"/index.md", "w") as f
      f.write(md)

#print (df['hospital_pk'].unique()[:10])
