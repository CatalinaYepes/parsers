# -*- coding: utf-8 -*-
"""
Testing code
"""
import pandas as pd

from parsers_exposure.mapping import mapping_matrix
from parsers_exposure.variable_1 import parse_1var
from parsers_exposure.variable_3 import census_3var_Crossed
from parsers_exposure import variable_2
from parsers_exposure.get_values import reshape_expo_data


#%% TEST 1 VARIABLE
data_file = '../ex_data-noncrossed.xlsx'
data = pd.read_excel(data_file, sheetname='variable_1')
mapping = mapping_matrix(data_file, num_variables='one', sheetname='mapping_1v', header=1)
result_1var = parse_1var(data, mapping)

print result_1var.head(5)


#%% TEST 2 VARIABLES - NON-CROSSED VARS
data_file = '../ex_data-noncrossed.xlsx'
data_var1 = pd.read_excel(data_file, sheetname=0)
data_var2 = pd.read_excel(data_file, sheetname=1)
mapping = mapping_matrix(data_file, num_variables='two', sheetname='mapping_1v_2v', header=1)

result_2var = variable_2.parse_2var_NonCrossed(data_var1, data_var2, mapping)

print result_2var.head(5)


#%% TEST 2 VARIABLES - CROSSED VARS
data_file = '../ex_data-crossed.xlsx'
data = pd.read_excel(data_file, sheetname='data_2vars')
mapping = mapping_matrix(data_file, num_variables='two', sheetname='mapping_2var', header=2)

result_2var = variable_2.census_2var_Crossed(data, mapping)

print result_2var.head(5)


#%% TEST 3 VARIABLES - CROSSED VARS
data_file = '../ex_data-crossed.xlsx'
data = pd.read_excel(data_file, sheetname='data_3vars')
mapping = mapping_matrix(data_file, num_variables='three', row_var3=9, sheetname='mapping_3var', header=2)

result_3var = census_3var_Crossed(data, mapping)

print result_3var.head(5)