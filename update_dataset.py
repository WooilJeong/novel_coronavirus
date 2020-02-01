import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import pandas as pd

scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]

json_file_name = 'gspread-266617-f39ee6d19800.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)

gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1yZv9w9zRKwrGTaR-YzmAqMefw4wMlaXocejdxZaTs6w/htmlview?usp=sharing&sle=true#'
doc = gc.open_by_url(spreadsheet_url)

#
sheet_list = doc.worksheets()
sheet_nm = []
for i in sheet_list:
    sheet_nm.append(i.title)
print('The number of recent sheets :', len(sheet_list))

#
df_list = []
for i in sheet_nm:

    data = doc.worksheet(i).get_all_values()
    globals()[i] = pd.DataFrame(data[1:], columns=data[0])

    df_list.append(globals()[i])


rm_items = ['Jan22_12am','Jan22_12pm','Jan23_12pm']
for i in rm_items:
    sheet_nm.remove(i)

col_list=[
            'Province/State',
            'Country/Region',
            'Last Update',
            'Confirmed',
            'Deaths',
            'Recovered'
         ]


Jan28_11pm['Last Update']='1/28/2020 23:00'
Jan25_10pm['Last Update']='1/25/2020 10:00 PM'
Jan24_12pm['Last Update']='1/24/2020 12:00 PM'
Jan31_2pm['Last Update']='1/31/2020 14:00'


df = pd.DataFrame()
for i in sheet_nm:

    try:
        print('Complete :', i)
        globals()[i] = globals()[i][col_list]
        df = pd.concat([df, globals()[i]])

    except:
        print('Failed :', i)

df=pd.DataFrame(df,columns=col_list)
df.index = range(len(df))


import datetime

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

date_list

df['Last Update'] = date_list


# Replace spaces with zeros
df['Confirmed'] = df["Confirmed"].apply(lambda x: 0 if x=="" else x)
df['Deaths'] = df["Deaths"].apply(lambda x: 0 if x=="" else x)
df['Recovered'] = df["Recovered"].apply(lambda x: 0 if x=="" else x)
df['Province/State'] = df["Province/State"].apply(lambda x: 'None' if x=="" else x)

# Data type conversion
df['Last Update'] = pd.to_datetime(df['Last Update'])
df['Confirmed'] = pd.to_numeric(df['Confirmed'])
df['Deaths'] = pd.to_numeric(df['Deaths'])
df['Recovered'] = pd.to_numeric(df['Recovered'])

# Feature Engineering
df['D/C'] = (df['Deaths']/df['Confirmed'])*100
df['R/C'] = (df['Recovered']/df['Confirmed'])*100

df = df.fillna(0)

# Mac
# now = datetime.datetime.now()
# now = str(now)[:16]
# now = now.replace('-','_')

# df.to_csv('Data/Dataset_'+now+'.csv',index=False,encoding='utf-8')

# Win

df.to_csv('Data/Dataset.csv', index=False, encoding='utf-8')
