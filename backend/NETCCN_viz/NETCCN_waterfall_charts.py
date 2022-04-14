#!/usr/bin/env python
# coding: utf-8

# In[1]:


#----------Imports------------#
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import waterfall_chart
import numpy as np


#----------Reading data and  cleaning------------#
#loading Utilizations data https://3.basecamp.com/3947469/buckets/21045036/uploads/4693186121
utilizations= pd.read_csv("hhs_utilizations1.csv")

NETCCN= pd.read_excel("NETCCN_central_active_complete.xlsx",dtype={'site.fips':'object'})
NETCCN["StatusLogStatusReceived_Start"]=pd.to_datetime(NETCCN["StatusLogStatusReceived_Start"],format='%Y/%m/%d').dt.date
NETCCN["actualStartDate"]=pd.to_datetime(NETCCN["actualStartDate"],format='%Y/%m/%d').dt.date
NETCCN["StatusLogStatusActive_Complete"]=pd.to_datetime(NETCCN["StatusLogStatusActive_Complete"],format='%Y/%m/%d').dt.date


#choose the index of the hospital of interest
x=NETCCN.iloc[1]
provider_id= x['provider.num']
waterfall_start= x["StatusLogStatusReceived_Start"]-dt.timedelta(weeks = 2) #to visualize 2 weeks before the request
waterfall_end= x["StatusLogStatusActive_Complete"]+dt.timedelta(days = 7) #to visualize 7 days after the end
#############
# Comment the previous line and uncomment the next line if the deployment is not complete
############
#waterfall_end= x["actualStartDate"]+dt.timedelta(days = 7) #to visualize 7 days after the end



#data sorting and cleaning
utilizations = utilizations.sort_values(by="collection_week")
utilizations=utilizations.replace(-999999, 0) #replacing missing value 
utilizations['collection_week'] = pd.to_datetime(utilizations["collection_week"],format='%Y/%m/%d').dt.date

## Creating dataframe for specific hospital
Specific_Hospital= utilizations[utilizations['hospital_pk']==str(provider_id)]
Specific_Hospital=Specific_Hospital[(Specific_Hospital['collection_week'] >= waterfall_start) & 
                                    (Specific_Hospital['collection_week'] <= waterfall_end)]
pd.set_option('display.max_columns', None)

# creating new dataframe with only columns of interest from hhs data
Specific_Hospital_filtered= Specific_Hospital[["collection_week"]]
Specific_Hospital_filtered["inpatient_beds_used_covid_7_day_avg"]= Specific_Hospital["inpatient_beds_used_covid_7_day_sum"]/7
Specific_Hospital_filtered["staffed_icu_adult_patients_confirmed_covid_7_day_avg"]= Specific_Hospital["staffed_icu_adult_patients_confirmed_covid_7_day_sum"]/7
Specific_Hospital_filtered["total_covid_patients"]= Specific_Hospital_filtered["inpatient_beds_used_covid_7_day_avg"]+Specific_Hospital_filtered["staffed_icu_adult_patients_confirmed_covid_7_day_avg"]
# setting the date as the index
Specific_Hospital_filtered= Specific_Hospital_filtered.set_index("collection_week")

#calculating detlas for each week (difference between current week and previous week)
deltas = [Specific_Hospital_filtered['total_covid_patients'][i] if 
          i==0 else Specific_Hospital_filtered['total_covid_patients'][i]-Specific_Hospital_filtered['total_covid_patients'][i-1] 
          for i in range(len(Specific_Hospital_filtered))]
# adding deltas as column to dataframe         
Specific_Hospital_filtered['delta'] = deltas
Specific_Hospital_filtered=Specific_Hospital_filtered.reset_index()



#--------Creating the waterfall chart-----------#

plt.rcParams["figure.figsize"] = (10,8)
#plotting the waterfall chart
ax=waterfall_chart.plot(Specific_Hospital_filtered["collection_week"], Specific_Hospital_filtered['delta'], 
                
                     formatting=" {:,.1f}",
                     net_label='Final \nnumber of patients',
                     
                     blue_color='royalblue', 
                     green_color='seagreen', red_color='tomato')
plt.title('Number of COVID-19 patients in '+ Specific_Hospital.iloc[0]["hospital_name"].lower().title()+'\n(weekly average) (inpatient beds + Staffed ICU beds)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
# adding the text for request week, start week and end week
####################
# the first parameter of ax.text is the xtick where you want the text to appear
# the second parameter of ax.text is the ytick where you want the text to appear
####################
ax.text(2,-0.5,"Week of \n the request",va='top', ha='center',fontweight='bold',color='royalblue')
ax.text(7,-0.25,"Week of\nthe start of\nthe engagement",va='top', ha='center',fontweight='bold',color='royalblue')
############ Comment next line if deployment is still active 
ax.text(15,1,"Week of\nthe end of\nthe engagement",va='top', ha='center',fontweight='bold',color='royalblue')
plt.ylabel('Average number of patients', fontsize=12)
sns.despine()

plt.savefig('Waterfall charts/'+Specific_Hospital.iloc[0]["hospital_name"].lower().title()+'.png', bbox_inches='tight')






