import pandas as pd
#import numpy as np

def extend_date_feature(df : pd.DataFrame, column_name : str):
    '''
    Extract from date-time timestamp many time-related features
        Date, year, month, week of year number, day of week number, time, hour
    '''
    if df[column_name].dtype == '<M8[ns]':
        df[f'{column_name}_Date'] = df[column_name].dt.to_period('D')
        df[f'{column_name}_Year'] = df[column_name].dt.year
        df[f'{column_name}_Month'] = df[column_name].dt.month
        df[f'{column_name}_Week'] = df[column_name].dt.week # may use smarter fe : week of month or etc. e.g.
        df[f'{column_name}_DOW'] = df[column_name].dt.dayofweek
        df[f'{column_name}_Hour'] = df[column_name].dt.hour
        df[f'{column_name}_Time'] = df[column_name].dt.time
    return df
