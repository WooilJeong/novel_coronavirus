import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import chart_studio
plotly_key=open(".plotly_key").read()
chart_studio.tools.set_credentials_file(username='coronavirus', api_key=plotly_key)
import chart_studio.plotly as py
import plotly.express as px

#
file_list = glob.glob("Data/*")
file_list = sorted(file_list, reverse=True)

#
try:
    df = pd.read_csv(file_list[0])
except:
    df = pd.read_csv(file_list[0].replace('\\','/')+'.csv')


print("Dataset Complete")

#
def agg(df):
    '''
    국가 및 지역 별 데이터 집계 함수
    '''

    df_region = df.groupby('Last Update').agg(
        {'Confirmed':['sum'], 'Death':['sum'],'Recovered':['sum']}).reset_index()

    df_region.index = range(len(df_region))
    df_region.columns=['Last Update', 'Confirmed', 'Death', 'Recovered']

    return df_region

df_all = agg(df)

#
fig = px.scatter_mapbox(df,
                        title='World New Coronavirus Chart',
                        lat="Lat",
                        lon="Long",
                        center={'lat':31, 'lon':112},
                        color="Country/Region",
                        size="Confirmed",
                        hover_name="Province/State",
                        animation_frame= "Last Update",
                        animation_group ="Province/State",
                        color_continuous_scale = px.colors.cyclical.IceFire,
                        template='plotly_dark',
                        size_max=75,
                        zoom=4)

fig.update_layout(showlegend=False)
py.plot(fig, filename='corona_scatter')

print("World New Coronavirus Chart Complete")

#
data = df_all.copy()
data_melt = data.melt(id_vars='Last Update', value_vars=['Death', 'Recovered'])

fig = px.line(data, x="Last Update", y="Confirmed", template='plotly_dark', title='Total Confirmed', text='Confirmed')
fig2= px.line(data_melt, x="Last Update", y="value", color='variable', template='plotly_dark', title='Total Death and Recovered', text='value')

fig.update_traces(textposition='top center')
fig.update_layout(legend_orientation="h")

py.plot(fig, filename='corona_confirmed')

print("Total Confirmed Complete")

#
fig2.update_traces(textposition='top center')
fig2.update_layout(legend_orientation="h")

py.plot(fig2, filename='corona_death_recovered')

print("Total Death and Recovered Complete")


#
# 모든 국가 리스트
country_list = list(set(df['Country/Region']))

# 제외할 국가 리스트(제외 국가는 세부 지역 별 리스트 생성하여 분석)
except_list = ['Mainland China', 'US', 'Canada', 'Australia']

# 세계 국가 리스트 재정의(일부 국가 제외)
world_list = country_list.copy()
for i in except_list:
    world_list.remove(i)

# 일부 국가(세부 지역 별 리스트 생성)
## 중국 지역 리스트
china_list = list(set(df[df['Country/Region']=='Mainland China']['Province/State']))
### 후베이 제외 중국 지역 리스트
china_list2 = china_list.copy()
china_list2.remove('Hubei')

## 미국 지역 리스트
us_list = list(set(df[df['Country/Region']=='US']['Province/State']))

## 캐나다 지역 리스트
canada_list = list(set(df[df['Country/Region']=='Canada']['Province/State']))

## 호주 지역 리스트
australia_list = list(set(df[df['Country/Region']=='Australia']['Province/State']))

for i in country_list:
    globals()[i.replace(' ','_')] = df[df['Country/Region']==i]
    globals()[i.replace(' ','_')] = globals()[i.replace(' ','_')].sort_values('Last Update', ascending=True)
    globals()[i.replace(' ','_')].index = range(len(globals()[i.replace(' ','_')]))
    # print(i.replace(' ','_'))

for i in china_list:
    globals()[i.replace(' ','_')] = Mainland_China[Mainland_China['Province/State']==i]
    globals()[i.replace(' ','_')] = globals()[i.replace(' ','_')].sort_values('Last Update', ascending=True)
    globals()[i.replace(' ','_')].index = range(len(globals()[i.replace(' ','_')]))

for i in us_list:
    globals()[i.replace(' ','_')] = US[US['Province/State']==i]
    globals()[i.replace(' ','_')] = globals()[i.replace(' ','_')].sort_values('Last Update', ascending=True)
    globals()[i.replace(' ','_')].index = range(len(globals()[i.replace(' ','_')]))
    # print(i.replace(' ','_'))

for i in australia_list:
    globals()[i.replace(' ','_')] = Australia[Australia['Province/State']==i]
    globals()[i.replace(' ','_')] = globals()[i.replace(' ','_')].sort_values('Last Update', ascending=True)
    globals()[i.replace(' ','_')].index = range(len(globals()[i.replace(' ','_')]))
    # print(i.replace(' ','_'))

for i in canada_list:
    globals()[i.replace(' ','_')] = Canada[Canada['Province/State']==i]
    globals()[i.replace(' ','_')] = globals()[i.replace(' ','_')].sort_values('Last Update', ascending=True)
    globals()[i.replace(' ','_')].index = range(len(globals()[i.replace(' ','_')]))
    # print(i.replace(' ','_'))


x_max = int(np.max(Mainland_China['Recovered']) * 1.2)
y_max = int(np.max(Mainland_China['Death']) * 1.2)

fig = px.scatter(Mainland_China,
               x="Recovered",
               y="Death",
               color='Province/State',
               title='Chinese New Coronavirus Chart',
               template='plotly_dark',
               log_x= False,
               animation_frame= "Last Update",
               animation_group ="Province/State",
               hover_name='Province/State',
               range_x = [-50,x_max],
               range_y = [-50,y_max],
               size='Confirmed',
               size_max=50,
               labels = dict(Death='Death',
                             Recovered = 'Recovered'))

fig.update_layout(showlegend=False)
py.plot(fig, filename='corona')

print("Chinese New Coronavirus Chart Complete")


time_list = list(set(df['Last Update']))
time_list = pd.DataFrame(time_list, columns=['Last Update']).sort_values('Last Update')
time_list.index = range(len(time_list))

total_list=world_list+china_list+us_list+australia_list+canada_list

for i in total_list:
    i=i.replace(' ','_')
    time_list=pd.merge(time_list, globals()[i][['Last Update', 'Confirmed']], how='left', on='Last Update')
time_list.columns=['Last Update']+total_list
time_list=time_list.fillna(0)

df_world = time_list[['Last Update']+world_list]
df_china = time_list[['Last Update']+china_list]
df_china2 = time_list[['Last Update']+china_list2]
df_us = time_list[['Last Update']+us_list]
df_australia = time_list[['Last Update']+australia_list]
df_canada = time_list[['Last Update']+canada_list]


data = df_world.copy()
data_melt=data.melt(id_vars='Last Update', value_vars=world_list)
fig=px.line(data_melt,
            x='Last Update',
            y='value',
            color='variable',
            title='Number of virus confirmed by country',
            template='plotly_dark')

fig.update_layout(showlegend=False)
py.plot(fig, filename='corona_world')

print("Number of virus confirmed by country Complete")


data = df_china.copy()
data_melt=data.melt(id_vars='Last Update', value_vars=china_list)
fig=px.line(data_melt,
            x='Last Update',
            y='value',
            color='variable',
            title='Number of virus confirmed (China)',
            template='plotly_dark')

fig.update_layout(showlegend=False)
py.plot(fig, filename='corona_china')

print("Number of virus confirmed (China) Complete")


data = df_china2.copy()
data_melt=data.melt(id_vars='Last Update', value_vars=china_list2)
fig=px.line(data_melt,
            x='Last Update',
            y='value',
            color='variable',
            title='Number of virus confirmed (China without Hubei)',
            template='plotly_dark'
           )
fig.update_layout(showlegend=False)
py.plot(fig, filename='corona_china_without_hubei')

print("Number of virus confirmed (China without Hubei) Complete")


data = df_us.copy()
data_melt=data.melt(id_vars='Last Update', value_vars=us_list)
fig=px.line(data_melt,
            x='Last Update',
            y='value',
            color='variable',
            title='Number of virus confirmed (US)',
            template='plotly_dark'
           )
fig.update_layout(showlegend=False)
py.plot(fig, filename='corona_us')

print("Number of virus confirmed (US) Complete")


data = df_australia.copy()
data_melt=data.melt(id_vars='Last Update', value_vars=australia_list)
fig=px.line(data_melt,
            x='Last Update',
            y='value',
            color='variable',
            title='Number of virus confirmed (Australia)',
            template='plotly_dark'
           )
fig.update_layout(showlegend=False)
py.plot(fig, filename='corona_australia')

print("Number of virus confirmed (Australia) Complete")


data = df_canada.copy()
data_melt=data.melt(id_vars='Last Update', value_vars=canada_list)
fig=px.line(data_melt,
            x='Last Update',
            y='value',
            color='variable',
            title='Number of virus confirmed (Canada)',
            template='plotly_dark'
           )
fig.update_layout(showlegend=False)
py.plot(fig, filename='corona_canada')

print("Number of virus confirmed (Canada) Complete")

print(">>> Update Complete")
