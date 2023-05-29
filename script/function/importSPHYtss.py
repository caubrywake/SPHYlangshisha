# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 16:32:48 2023

@author: carol
"""

import datetime
import pandas as pd

def importtss(start_year, start_month, start_day, input_file, colname):
    """
    start_year = '2013'
    start_day = '01'
    start_month ='01'
    input_file = 'C:/SPHY3/output/20230313/QAllDTS.tss'
    colname =  ['Outlet', 'GW 1', 'GW 2', 'GW 3', 'AWS']
    """
    # start of simulation
    start_date = datetime.datetime.strptime(start_month + '/' + start_day + '/' + start_year, "%m/%d/%Y")

    var = []
    days = []

    with open(input_file, 'r') as f:
        for line_number, line in enumerate(f, 1):
            if line_number > 8:
                data = line.split()
                x = int(data[0])
                y = list(map(float, data[1:]))
                var.append(y)
                days.append(start_date + datetime.timedelta(days=x))
      
        df = pd.DataFrame(var,columns= colname)
        dt = pd.DataFrame(days,columns= ['datetime'])
        df_concat =  pd.concat([dt, df], axis = 1)
        df_concat.set_index('datetime', inplace=True)
    return df_concat
