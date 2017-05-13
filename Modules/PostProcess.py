# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 14:17:47 2016

@author: swang
"""

import pandas as pd
import numpy as np


def MergeTable(df1, df2, Date):
    df3= pd.merge(df1, df2, how='left', on=['index'])
    df3['hour'] = [int(time/3600) for time in df3.timestamp]
    df3['flag'] = df3.C1 | df3.C2 | df3.C3 | df3.C4 | df3.C5 | df3.C6 | df3.C7 | df3.C8 | df3.C10 | df3.CX1
    df3.loc[df3.flag.isnull==True, 'flag']= 0
    df3.to_csv('./OutputTable/' + Date + 'FinalDF.csv')
    
    return df3


def PostByTime(df3, Date):
    c1 = df3.pivot_table(index='detector_id', columns='hour', values='flag', aggfunc='sum')
    c2 = df3.pivot_table(index='detector_id', columns='hour', values='flag',aggfunc='count')
    ccs = pd.concat([c1,c2], axis=1)
    ccs.to_csv('./OutputTable/' + Date + 'ByTime.csv')
    
    return ccs

def PostByCriteria(df3, Date):    
    a1 = df3.pivot_table(index='detector_id',  values='C1',aggfunc='sum')
    a2 = df3.pivot_table(index='detector_id',  values='C2',aggfunc='sum')
    a3 = df3.pivot_table(index='detector_id',  values='C3',aggfunc='sum')
    a4 = df3.pivot_table(index='detector_id',  values='C4',aggfunc='sum')
    a5 = df3.pivot_table(index='detector_id',  values='C5',aggfunc='sum')
    a6 = df3.pivot_table(index='detector_id',  values='C6',aggfunc='sum')
    a7 = df3.pivot_table(index='detector_id',  values='C7',aggfunc='sum')
    a8 = df3.pivot_table(index='detector_id',  values='C8',aggfunc='sum')
    a10 = df3.pivot_table(index='detector_id',  values='C10',aggfunc='sum')
    aX1 = df3.pivot_table(index='detector_id',  values='CX1',aggfunc='sum')
    
    b1 = df3.pivot_table(index='detector_id',  values='flag',aggfunc='sum')
    b2 = df3.pivot_table(index='detector_id',  values='flag',aggfunc='count')
    
    aabbs = pd.concat([a1,a2,a3,a4,a5,a6,a7,a8,a10,aX1,b1,b2], axis=1)
    aabbs.to_csv('./OutputTable/' + Date + 'ByCriteria.csv')
    
    return aabbs
    
def PostByDate(Dates): 
    for Date in Dates:
        df_f = pd.read_table('./OutputTable/' + Date + 'FinalDF.csv',sep=',')
        df_c1 = df_f.pivot_table(index='detector_id', values='flag', aggfunc='sum')
        df_c2 = df_f.pivot_table(index='detector_id', values='flag', aggfunc='count')
        df_c3 = np.array(map(float,df_c1.values))/np.array(map(float, df_c2.values))
        
        df_cc = pd.DataFrame({'detector_id':[]}) # new data frame
        df_cc['detector_id']=df_c1.index.values # add columns
        df_cc['flags']=df_c3
        df_cc['Date']= np.array([Date] * len(df_cc))
        
        if Date == Dates[0]: df_Summary = df_cc
        if Date <> Dates[0]: df_Summary = pd.concat([df_Summary,df_cc], axis=0)
    
        del df_c1, df_c2, df_c3, df_cc
    
    df_Summary1 = df_Summary.pivot_table(index='detector_id', columns='Date', values='flags', aggfunc='sum')    
    df_Summary1.to_csv('./OutputTable/' + 'SummaryDF1.csv')
    
    return df_Summary1