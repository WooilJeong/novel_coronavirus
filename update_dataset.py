print(">>> Start")

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
json_file_name = 'gspread-266617-7512230df225.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)

gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1UF2pSkFTURko2OvfHWWlFpDFAr1UxCBA4JLwlSP6KFo/htmlview?usp=sharing&sle=true#'
doc = gc.open_by_url(spreadsheet_url)

sheet_list = doc.worksheets()
sheet_nm = []
for i in sheet_list:
    sheet_nm.append(i.title)

print('sheets number :', len(sheet_list))
print(sheet_nm)

df_list = []
for i in sheet_nm:
    print(i)
    data = doc.worksheet(i).get_all_values()
    globals()[i] = pd.DataFrame(data[1:], columns=data[0])

    del globals()[i][globals()[i].columns[2]]

    df_list.append(globals()[i])


id_vars=['Province/State',
         'Country/Region',
         'Lat',
         'Long'
         ]

for i in sheet_nm:
    globals()['df_'+i] = pd.melt(globals()[i],
                                 id_vars=id_vars,
                                 var_name='Last Update',
                                 value_name=i,
                                ).sort_values('Last Update', ascending=True)
    globals()['df_'+i].index=range(len(globals()['df_'+i]))

df = pd.merge(df_Confirmed, df_Death, how='left')
df = pd.merge(df, df_Recovered, how='left')

date_list=[]
for i in df['Last Update']:

    if 'AM' in i:

        a=datetime.datetime.strptime(i, "%m/%d/%Y %I:%M %p")
        b=datetime.datetime.strftime(a, "%Y-%m-%d %H:%M")

    elif 'PM' in i:

        a=datetime.datetime.strptime(i, "%m/%d/%Y %I:%M %p")
        b=datetime.datetime.strftime(a, "%Y-%m-%d %H:%M")

    else:

        a=datetime.datetime.strptime(i, "%m/%d/%Y %H:%M")
        b=datetime.datetime.strftime(a, "%Y-%m-%d %H:%M")

    date_list.append(b)

df['Last Update'] = date_list

# Replace spaces with zeros
df['Province/State'] = df["Province/State"].apply(lambda x: 'None' if x=="" else x)
df['Confirmed'] = df["Confirmed"].apply(lambda x: 0 if x=="" else x)
df['Death'] = df["Death"].apply(lambda x: 0 if x=="" else x)
df['Recovered'] = df["Recovered"].apply(lambda x: 0 if x=="" else x)

# ETC
df['Confirmed'] = df["Confirmed"].apply(lambda x: 0 if x=="`" else x)

# Data type conversion
df['Lat'] = pd.to_numeric(df['Lat'])
df['Long'] = pd.to_numeric(df['Long'])
df['Last Update'] = pd.to_datetime(df['Last Update'])
df['Confirmed'] = pd.to_numeric(df['Confirmed'])
df['Death'] = pd.to_numeric(df['Death'])
df['Recovered'] = pd.to_numeric(df['Recovered'])

# Feature Engineering
df['D/C'] = (df['Death']/df['Confirmed'])*100
df['R/C'] = (df['Recovered']/df['Confirmed'])*100

# Fill Na with Zeros
df = df.fillna(0)

df=df.sort_values('Last Update', ascending=True)

if not os.path.exists('Data'):
    os.mkdir('Data')

df.to_csv('Data/Dataset.csv',index=False,encoding='utf-8')

print(">>> Complete")
