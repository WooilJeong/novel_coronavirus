def agg(df):
    '''
    국가 및 지역 별 데이터 집계 함수
    '''

    df_region = df.groupby('Last Update').agg(
        {'Confirmed':['sum'], 'Deaths':['sum'],'Recovered':['sum']}).reset_index()
    
    df_region.index = range(len(df_region))
    df_region.columns=['Last Update', 'Confirmed', 'Deaths', 'Recovered']
    
    # Feature Engineering
    df_region['D/C'] = (df_region['Deaths']/df_region['Confirmed'])*100
    df_region['R/C'] = (df_region['Recovered']/df_region['Confirmed'])*100
    
    return df_region