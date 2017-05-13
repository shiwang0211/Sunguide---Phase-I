# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 13:30:39 2016

@author: swang
"""
import pandas as pd
global pd

def ReadRawData(Date):

    df_Raw = pd.read_table('./Rawdat/TSS-'+ Date +'2016--1.dat',sep=', ')
    Config = pd.read_table('./Configuration/configuration.csv',sep=',')
    df_Raw.speed = pd.to_numeric(df_Raw.speed, errors='coerce')
    df_Raw.volume = pd.to_numeric(df_Raw.volume, errors='coerce')
    df_Raw.occupancy = pd.to_numeric(df_Raw.occupancy, errors='coerce')
    df_Raw.lane_id = [int(lane_id_string.split(':')[0]) for lane_id_string in df_Raw.lane_id]
    df_Raw.detector_id = [int(detector_id_string.split(':')[0]) for detector_id_string in df_Raw.detector_id]
                 
    hour = [int(time.split(':')[0]) for time in df_Raw.timestamp]
    minu = [int(time.split(':')[1]) for time in df_Raw.timestamp]
    seco = [int(time.split(':')[2]) for time in df_Raw.timestamp]
    times = [0.0]* len(hour)                 
    for i in xrange(len(hour)):
        times[i] = 3600 * hour[i] + 60 * minu[i] + 1 * seco[i]; 
        if seco[i] >= 0 and seco[i] <15: times[i] -= seco[i];
        if seco[i] >= 15 and seco[i] <30: times[i] += (30 - seco[i]);
        if seco[i] >= 30 and seco[i] <45: times[i] -= (seco[i]-30);
        if seco[i] >= 45 and seco[i] <60: times[i] += (60 - seco[i]);
    df_Raw.timestamp = times
    
    df_Raw = df_Raw.loc[:,['detector_id','lane_id','timestamp','volume','occupancy','speed']]    
    df = pd.merge(df_Raw, Config, how='left', on=['detector_id', 'lane_id'])
    
    # to fix mismatch of no. of lanes
    del df['NO_LANES']
    Config_v2 = Config[['detector_id','NO_LANES']]
    Config_v2 = Config_v2.drop_duplicates()
    #Config_v2['detector_id'].value_counts()
    df2 = pd.merge(df, Config_v2, how='left', on=['detector_id']) 
    #df2['NO_LANES'].value_counts()
    #df.loc[pd.isnull(df2['NO_LANES'])]
    
    #df2.to_csv('./AfterStep1/TSS-' + Date + '2016--1 - step1.csv')
    return df2