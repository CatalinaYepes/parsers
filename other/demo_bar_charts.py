# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 16:57:55 2015

@author: catalinayepes
"""

import plotly as py
import pandas as pd
import numpy as np

name = 'level_0/per-l0'
exposure = pd.read_csv(name +'-exposure.csv')
new_exposure = simplify_taxonomy(exposure, 'modify_taxonomy.csv')
per0 = aggregate_exposure(new_exposure)

data = ecu0.append([col0,per0])
data.drop('Region',1,inplace=True)
data.drop('Dwellings',1,inplace=True)

legend = [u'CR/LFM-LFINF', u'CR/LWAL-LDUAL', u'ER+ETR', u'MCF', u'MR', u'MUR', u'MUR+ADO', u'MUR+ST', u'UNK', u'W']
serie1 = [1161332, 160956, 381440.0, 1898759.7,
       373854.65, 4004629, 190720.0, 97374.0, 62686.0,
       1411204]
toPlot = np.array(data)


info = py.graph_objs.Data([py.graph_objs.Bar(x =legend, y=serie1 )])