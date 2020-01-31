def agg(df):
    '''
    국가 및 지역 별 데이터 집계 함수
    '''

    df_region = df.groupby('Last Update').agg(
        {'Confirmed':['sum']}).reset_index()
    
    df_region.index = range(len(df_region))
    df_region.columns=['Last Update', 'Confirmed']
    
    return df_region