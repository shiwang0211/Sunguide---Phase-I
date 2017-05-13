# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 14:09:16 2016

@author: swang
"""

import pandas as pd
import numpy as np


def CriteriaCalculation(df):
    
    
    C1 = np.array([0]* len(df))
    C2 = np.array([0]* len(df))
    C3 = np.array([0]* len(df))
    C4 = np.array([0]* len(df))
    C5 = np.array([0]* len(df))
    C6 = np.array([0]* len(df))
    C7 = np.array([0]* len(df))
    C8 = np.array([0]* len(df))
    C10 = np.array([0]* len(df))
    CX1 = np.array([0]* len(df))
    
    
    df1 = df.sort(['detector_id', 'DIRECTION','lane_id','timestamp'])
    
    occupancy = np.array(df1.occupancy)
    speed = np.array(df1.speed)
    volume = np.array(df1.volume)
    timestamp = np.array(df1.timestamp)
    lane_id = np.array(df1.lane_id)
    detector_id = np.array(df1.detector_id)
    SPEED_LIMIT = np.array(df1.SPEED_LIMIT)
    L = len(df1)
    
    #----------------C1, C2,C5, C7, CX1-------------------------------------------------------------
    
    for currentRow in xrange(0,L):
        C2[currentRow] = 1 if occupancy[currentRow]>90 else 0;
        C5[currentRow] = 1 if (speed[currentRow]<3) & (volume[currentRow]>2) else 0
        CX1[currentRow] = 1 if ((speed[currentRow]<(SPEED_LIMIT[currentRow]-10)) & (volume[currentRow]<8) & (occupancy[currentRow]<15)) else 0
     
    
    for currentRow in xrange(0,L-1):
    	Condition1 = ((timestamp[currentRow+1] -  timestamp[currentRow])==29) | ((timestamp[currentRow+1] -  timestamp[currentRow])==30) | ((timestamp[currentRow+1] -  timestamp[currentRow])==31)
    	Condition2 = (volume[currentRow+1] +  volume[currentRow]) > 50
    	if(Condition1 & Condition2): C1[currentRow]=1;
    	if(Condition1 & Condition2): C1[currentRow+1]=1;
    
    
              
    PERIOD = 8;
    for currentRow in xrange(0,L-PERIOD):
        four_mins = np.array(xrange(currentRow, currentRow + PERIOD));
        Condition1 = lane_id[currentRow + PERIOD - 1] == lane_id[currentRow];
        Condition2 = min(volume[four_mins]) == max(volume[four_mins]);
        Condition3 = min(volume[four_mins]) > 0
        if(Condition1 & Condition2 & Condition3): C7[four_mins] = 1;
    
         
    #------------------C3, C4,C6, C8, C10------------------------------------------------------------
    
    df2 = df.sort(['detector_id', 'timestamp','DIRECTION','lane_id'])        
     
    occupancy = np.array(df2.occupancy)
    speed = np.array(df2.speed)
    volume = np.array(df2.volume)
    timestamp = np.array(df2.timestamp)
    lane_id = np.array(df2.lane_id)
    detector_id = np.array(df2.detector_id)
    DIRECTION = np.array(df2.DIRECTION)
    NO_LANES = np.array(df2.NO_LANES)
    SPEED_LIMIT = np.array(df2.SPEED_LIMIT)
    L = len(df2)
    
    Rowindex=[]
    speeds=[]
    for currentRow in xrange(0,L-1):
        
        if(Rowindex==[]):
            Condition2 = 0;
            Condition3 = 0;
            error_count = 0;
            speeds=[]
        
        Rowindex.append(currentRow);
        if (not(np.isnan(speed[currentRow]))):   
            speeds.append(speed[currentRow])
       
        Condition1 = (timestamp[currentRow+1] <> timestamp[currentRow]) |  (detector_id[currentRow+1] <> detector_id[currentRow]) | (DIRECTION[currentRow+1] <>  DIRECTION[currentRow]) | (currentRow ==(L-1))
       
        if((len(speeds)>3) & Condition1):
            a = (sorted(speeds)[-2]-sorted(speeds)[0])>35
            b = (sorted(speeds)[-1]-sorted(speeds)[0])>35
            c = (sorted(speeds)[-2]-sorted(speeds)[1])>35
            d = (sorted(speeds)[-1]-sorted(speeds)[1])>35
            error_count = int(a)+int(b)+int(c)+int(d);
                           
        if((len(speeds)==3) & Condition1):
            a = (sorted(speeds)[-2]-sorted(speeds)[0])>35
            b = (sorted(speeds)[-1]-sorted(speeds)[0])>35
            c = (sorted(speeds)[-2]-sorted(speeds)[1])>35
            error_count = int(a)+int(b)+int(c);                  
                          
        Condition2 = 1 if (error_count >= 2) else Condition2;
        Condition3 = (np.nanmin(speed[Rowindex]) >=35) & (np.nanmin(speed[Rowindex]) > (SPEED_LIMIT[Rowindex[0]] + 25))
        
        if(Condition1 & Condition2): C3[Rowindex] = 1;
        if(Condition1 & Condition3): C4[Rowindex] = 1;
        if(Condition1):
            Rowindex=[];
            error_count = 0;
    
    
    
    Rowindex=[]
    for currentRow in xrange(0,L-1):
        if(Rowindex==[]):
            Condition61 = 0;
            Condition62 = 0;
            Condition63 = 0;
            Condition64 = 0;
            
        Rowindex.append(currentRow);
        Condition1 = (timestamp[currentRow+1] <> timestamp[currentRow]) |  (detector_id[currentRow+1] <> detector_id[currentRow]) | (currentRow ==(L-1))
                 
        Condition61 = 1 if((occupancy[currentRow] < 3) & (speed[currentRow] < 45)) else Condition61;
        Condition62 = 1 if((speed[currentRow] > 0) &  (volume[currentRow] == 0)) else Condition62;
        Condition63 = 1 if((speed[currentRow] == 0) & (volume[currentRow] > 0)) else Condition63;
        Condition64 = 1 if((occupancy[currentRow] > 70) & (volume[currentRow] == 0)) else Condition64;
        
        Condition6 = Condition61 | Condition62 | Condition63 | Condition64;
        
        if(Condition1 & Condition6):  C6[Rowindex] = 1;
        if(Condition1): 
            Rowindex=[];
            Condition6=0
    
        
    
    
    Rowindex1=[];  
    Rowindex2=[];  
    N_item_list=[];
    same_volume=0;
    PERIOD = 8;
      
    for currentRow in xrange(0,L-1):
        
        Rowindex1.append(currentRow);
        Condition0 = detector_id[currentRow+1] <> detector_id[currentRow];
        Condition1 = Condition0 | ((timestamp[currentRow+1] <> timestamp[currentRow]) &  (detector_id[currentRow+1] == detector_id[currentRow]))
       
        Condition21 = min(volume[Rowindex1]) == max(volume[Rowindex1])
        Condition22 = min(volume[Rowindex1]) > 0
        Condition23 = NO_LANES[currentRow]>1
        Condition2 = Condition21 & Condition22 & Condition23
        
        if(Condition1):
            N_item_list.append(len(Rowindex1))
            Rowindex2 = Rowindex2 + Rowindex1;
            Rowindex1=[];
        
        Condition3 = len(N_item_list)>PERIOD;
        
        if(Condition1 & Condition2): same_volume += 1;
        if(Condition1 & (not(Condition2))): same_volume = 0;
        if(Condition1 & Condition3): 
            del Rowindex2[0:N_item_list[0]];
            del N_item_list[0];
        if(Condition1 & (same_volume >= PERIOD)): C8[Rowindex2] = 1;
        if(Condition0): 
            Rowindex1=[]
            Rowindex2=[]
            N_item_list=[]
            same_volume=0
    
        
        
    Rowindex=[]; 
    lane_count = 0;
    lanes=[]
    
    for currentRow in xrange(0,L-1):
      
        lanes.append(lane_id[currentRow]) 
        Rowindex.append(currentRow);
        Condition0 = detector_id[currentRow+1] <> detector_id[currentRow]
        Condition1 = Condition0 | ((timestamp[currentRow+1] <> timestamp[currentRow]) &  (detector_id[currentRow+1] == detector_id[currentRow]))
        
        lane_count = len(set(list(lanes)))
        Condition2 = (lane_count <> NO_LANES[currentRow])
        
        if(Condition1 & Condition2): C10[Rowindex] = 1;
        
        if(Condition1):
            lane_count = 0
            Rowindex=[]
            lanes=[]
            Condition2=0
      
            
    #------------------Append to data table-------------
        
    df1['C1'] = C1
    df1['C2'] = C2
    df1['C5'] = C5
    df1['C7'] = C7
    df1['CX1'] = CX1
    
    df2['C3'] = C3
    df2['C4'] = C4
    df2['C6'] = C6
    df2['C8'] = C8
    df2['C10'] = C10
    
    df1['index'] = df1.index
    df2['index'] = df2.index
    df2 = df2.loc[:,['index','C3','C4','C6','C8','C10']]
            
    return C1, C2, C3, C4, C5, C6, C7, C8, C10, CX1, df1, df2