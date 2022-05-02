#!/usr/bin/env python3
# coding: utf-8

import pandas as pd
import datetime as dt
import plotly.graph_objects as go
import plotly
import numpy as np
import os
import json

print("loading all hospital info")
hospitals = pd.read_csv("/mnt/scratch/datasources/netccn/Hospital_for_Research_List.csv")
#ccn,hospital_name,address,city,state,zip,fips_code,hospital_subtype,is_metro_micro,total_beds_7_day_avg,total_icu_beds_7_day_avg,RUCC_2013,Description,E_TOTPOP,EP_POV,E_PCI,EP_AGE65,EP_AGE17,EP_DISABL,EP_MINRTY,RPL_THEME1,RPL_THEME2,RPL_THEME3,RPL_THEME4,Latitude,Longitude

print("loading netccn central..")
NETCCN = pd.read_excel("/mnt/scratch/datasources/netccn/NETCCN_Central_active_complete.xlsx",dtype={'site.fips':'object'})

data = []

for index, row in hospitals.iterrows():
  print(index)
  #print(row)
  #ccn                                                                    431332
  #hospital_name                           AVERA DE SMET MEMORIAL HOSPITAL - CAH
  #address                            306 PRAIRIE AVENUE SW  POST OFFICE BOX 160
  #city                                                                  DE SMET
  #state                                                                      SD
  #zip                                                                     57231
  #fips_code                                                             46077.0
  #hospital_subtype                                    Critical Access Hospitals
  #is_metro_micro                                                          False
  #total_beds_7_day_avg                                                      6.0
  #total_icu_beds_7_day_avg                                                  0.0
  #RUCC_2013                                                                 9.0
  #Description                 Nonmetro - Completely rural or less than 2,500...
  #E_TOTPOP                                                                 4967
  #EP_POV                                                                    9.5
  #E_PCI                                                                   32259
  #EP_AGE65                                                                 22.4
  #EP_AGE17                                                                 22.0
  #EP_DISABL                                                                11.9
  #EP_MINRTY                                                                 3.1
  #RPL_THEME1                                                             0.0745
  #RPL_THEME2                                                             0.2324
  #RPL_THEME3                                                              0.028
  #RPL_THEME4                                                             0.0669
  #Latitude                                                             44.36152
  #Longitude                                                           -97.57204

  netccn = NETCCN[NETCCN["provider.num"]==row["ccn"]]

  hospital = {
    "id": row["ccn"],
    "title": row["hospital_name"],
    "address": row["address"],
    "city": row["city"],
    "state": row["state"],
    "zip": row["zip"],
    "fips": row["fips_code"],
    "hospitalSubtype": row["hospital_subtype"],
    "lat": row["Latitude"],
    "lng": row["Longitude"],
    "deployed": False
  }

  if len(netccn.index) == 1:
    #print(netccn.iloc[0])
    #id                                                152
    #provider.num                                   261329
    #Site.Name                         Cox-Monett-Hospital
    #site.fips                                       29009
    #StatusLogStatusReceived_Start     2022-01-11 00:00:00
    #actualStartDate                   2022-01-20 00:00:00
    #StatusLogStatusActive_Complete                    NaT
    #Name: 48, dtype: object
    if netccn.iloc[0]["site.fips"] != "0":
      hospital["deployed"] = True

#for index, row in NETCCN.iterrows():
#  fipscode = str(row["site.fips"])
#
#  #there is an entry with fipscode set to 0 for some reason
#  if fipscode == "0":
#    continue
#
#  #print(fipscode)
  data.append(hospital)

with open("../static/netccn/hospitals.json", "w") as f:
  json.dump(data, f, indent=4)

print("all done")


