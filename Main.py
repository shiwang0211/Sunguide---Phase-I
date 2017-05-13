import os
import sys
sys.path.append('Modules')
from ReadRawData_ import ReadRawData
from Criterias import CriteriaCalculation
from PostProcess import MergeTable,PostByTime,PostByCriteria,PostByDate
import pandas as pd
import numpy as np

os.chdir('../Deland')

Dates = ['1201','1202','1203','1204','1205','1206','1207','1208','1209','1210','1211','1212']

for Date in Dates: 
    df = ReadRawData(Date)
    C1, C2, C3, C4, C5, C6, C7, C8, C10, CX1, df1, df2 =  CriteriaCalculation(df)
    df3 = MergeTable(df1, df2, Date)
    Table1 = PostByTime(df3, Date)
    Table2 = PostByCriteria(df3, Date)
    
Table3 = PostByDate(Dates)
















