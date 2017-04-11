# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 13:06:31 2017

@author: catalinayepes
"""
import pandas as pd

def read_args(name, **kwds):
    data = pd.read_excel(name, **kwds)
    
    return data

    
name = 'example-data-noncrossed_variables.xlsx'
data = read_args(name, sheetname=0)

print data

#test = pd.read_excel('example-data-noncrossed_variables.xlsx', sheetname=0)
