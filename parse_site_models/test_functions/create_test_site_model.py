#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 12:26:46 2018

@author: cyepes
"""
import pandas as pd
from parse_site_models.build_site_model import write_site_model_file
from parse_site_models.build_site_model import site_model_to_NRML

vs30_df = pd.read_csv('example_vs30_data.csv', header=None, names=['lon','lat','vs30'])
exposure = pd.read_csv('example_exposure.csv')
sites_df = exposure.loc[:,['lon','lat']]
sitemodel_file = 'test_site_model.csv'


df_site_model = write_site_model_file(vs30_df, sites_df, sitemodel_file)
save_as = 'test_site_model.xml'
site_model_to_NRML(df_site_model, save_as)