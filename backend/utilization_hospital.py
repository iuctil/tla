import pandas as pd 
import os
import plotly.express as px
import plotly.graph_objects as go

df= pd.read_csv("/Users/mariemloukil/utilizations.csv", header=0,index_col=False)

df = df.sort_values(by="collection_week") #sorting dataset by year
hospitals_ids = df['hospital_pk'].unique() [0:4]# getting the unique hospital_pk
df=df.replace(-999999, -7) #replacing missing value 


# Parent Directory path
parent_dir = "/Users/mariemloukil/tla/content/hospitals"

for id in hospitals_ids:
    df_slice= df[df['hospital_pk']== id] #dataframe for each hospital
    path = os.path.join(parent_dir, str(id)) 
    os.mkdir(path) #creating a directory for each hospital
    df_slice.to_csv(path+ "/"+str(id)+"_utilization.csv",index=False) # saving each hospital data
    
  
for id in hospitals_ids:
    path = os.path.join(parent_dir, str(id))
    df_slice=pd.read_csv(path+ "/"+str(id)+"_utilization.csv")
    fig = go.Figure()
    #fig.add_trace(go.Scatter(x=df_slice["collection_week"], y=df_slice["inpatient_beds_7_day_avg"],
                   # mode='lines',
                   # name='average  inpatient beds'))
   # fig.add_trace(go.Scatter(x=df_slice["collection_week"], y=df["inpatient_beds_used_7_day_avg"],
                 #   mode='lines',
                  #  name='average inpatient beds  used'))
    fig.add_trace(go.Scatter(x=df_slice["collection_week"], y=df_slice["inpatient_beds_used_covid_7_day_sum"]/7,
                   mode='lines',
                   name='average inpatient beds used for COVID-19'))
    fig.add_trace(go.Scatter(x=df_slice["collection_week"], y=df_slice["staffed_icu_adult_patients_confirmed_covid_7_day_sum"]/7,
                   mode='lines',
                   name='average ICU beds used for COVID-19'))               
    fig.write_image(path+ "/"+str(id)+"_utilization_COVID19.png")
    fig.write_html(path+ "/"+str(id)+"_utilization_COVID19.html")
    fig.write_json(path+ "/"+str(id)+"_utilization_COVID19.json")
  


#print (df['hospital_pk'].unique()[:10])
