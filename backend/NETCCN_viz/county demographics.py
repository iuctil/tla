#!/usr/bin/env python
# coding: utf-8

# In[26]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# In[27]:


NETCCN= pd.read_excel("NETCCN_central_active_complete.xlsx")
NETCCN["StatusLogStatusReceived_Start"]=pd.to_datetime(NETCCN["StatusLogStatusReceived_Start"],format='%Y/%m/%d').dt.date
NETCCN["actualStartDate"]=pd.to_datetime(NETCCN["actualStartDate"],format='%Y/%m/%d').dt.date
NETCCN["StatusLogStatusActive_Complete"]=pd.to_datetime(NETCCN["StatusLogStatusActive_Complete"],format='%Y/%m/%d').dt.date
NETCCN.head()


# In[28]:


df=pd.read_csv("SVI2018_US_COUNTY.csv")
df.head()


# In[29]:


demographics= df[["STATE" ,"ST_ABBR", "COUNTY" ,"FIPS" ,"LOCATION" ,"AREA_SQMI","E_TOTPOP","E_POV", "E_UNEMP","E_AGE65","E_AGE17","E_DISABL","E_UNINSUR"]]
demographics.head()


# In[30]:


us_population= sum(demographics["E_TOTPOP"])
us_poverty= round((sum(demographics["E_POV"])/us_population)*100,1)
us_unemp= round((sum(demographics["E_UNEMP"])/us_population)*100,1)
us_age65= round((sum(demographics["E_AGE65"])/us_population)*100,1)
us_age17= round((sum(demographics["E_AGE17"])/us_population)*100,1)
us_disability= round((sum(demographics["E_DISABL"])/us_population)*100,1)
us_uninsured= round((sum(demographics["E_UNINSUR"])/us_population)*100,1)
print(us_poverty)


# In[31]:


for index, row in NETCCN.iterrows():
    county= demographics[demographics["FIPS"]==row["site.fips"]]
    county_population= county.iloc[0]["E_TOTPOP"]
    county_poverty=round((county.iloc[0]["E_POV"]/county_population)*100,1)
    county_unemp= round((county.iloc[0]["E_UNEMP"]/county_population)*100,1)
    county_age65= round((county.iloc[0]["E_AGE65"]/county_population)*100,1)
    county_age17= round((county.iloc[0]["E_AGE17"]/county_population)*100,1)
    county_disability=round((county.iloc[0]["E_DISABL"]/county_population)*100,1)
    county_uninsured= round((county.iloc[0]["E_UNINSUR"]/county_population)*100,1)
    
    state=demographics[demographics["STATE"]==county.iloc[0]["STATE"]]
    state_population= sum(state["E_TOTPOP"])
    state_poverty= round((sum(state["E_POV"])/state_population)*100,1)
    state_unemp= round((sum(state["E_UNEMP"])/state_population)*100,1)
    state_age65= round((sum(state["E_AGE65"])/state_population)*100,1)
    state_age17= round((sum(state["E_AGE17"])/state_population)*100,1)
    state_disability= round((sum(state["E_DISABL"])/state_population)*100,1)
    state_uninsured= round((sum(state["E_UNINSUR"])/state_population)*100,1)
                               
    plt.rcParams["figure.figsize"] = [10, 7.50]
    
    #plt.rcParams["figure.autolayout"] = True

    columns = ( county.iloc[0]["COUNTY"]+ " County", 'State: '+county.iloc[0]["STATE"].lower().title(), 'U.S.')

    cell_text = [[ "{:,}".format(county_population), "{:,}".format(state_population), "{:,}".format(us_population)],
    [ str(county_poverty)+'%', str(state_poverty)+'%', str(us_poverty)+'%'],
    [ str(county_unemp)+'%', str(state_unemp)+'%', str(us_unemp)+'%'],
    [ str(county_uninsured)+'%', str(state_uninsured)+'%', str(us_uninsured)+'%'],
    [ str(county_disability)+'%', str(state_disability)+'%', str(us_disability)+'%',],
    [ str(county_age65)+'%', str(state_age65)+'%', str(us_age65)+'%'],
    [ str(county_age17)+'%', str(state_age17)+'%', str(us_age17)+'%']
               ]
    rows= ["Population ","Percentage of Population below poverty","Percentage of Unemployed Population",
          "Percentage of Uninsured Population ","Percentage of Population with Disability","Percentage of Population Aged 65 and older",
          "Percentage of Population Aged 17 and younger"]
    rcolors = plt.cm.BuPu(np.full(len(rows), 0.1))
    ccolors = plt.cm.BuPu(np.full(len(columns), 0.1))
                     

    fig, ax = plt.subplots()

    the_table = ax.table(cellText=cell_text,rowLabels=rows,rowColours=rcolors,colColours=ccolors,
                     colLabels=columns, loc='right',cellLoc='center')
    ax.axis('off')
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(16)
    the_table.scale(1, 4)
    the_table.auto_set_column_width(col=list(range(len(columns)))) 
    plt.title(str(county.iloc[0]["COUNTY"])+" County Demographics", fontsize=20)
    plt.savefig('Demographics/'+str(county.iloc[0]["COUNTY"])+"_"+ str(county.iloc[0]["FIPS"])+'.png', bbox_inches='tight')
    plt.show()


# In[ ]:




