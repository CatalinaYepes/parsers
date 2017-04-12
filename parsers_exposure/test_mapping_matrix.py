# -*- coding: utf-8 -*-
"""
Testing code
"""
import pandas as pd

from mapping import mapping_matrix


mapping_file = 'ex_mapping_scheme.xlsx'
matrix = pd.read_excel(mapping_file, header=2, sheetname='mapping_2var')

#%% TESTING 1_VARIABLE
mp = mapping_matrix(mapping_file, num_variables='one', print_vars=True, sheetname='mapping_1var', header=1)

#%% TESTING 2_VARIABLES
mp = mapping_matrix(mapping_file, num_variables='two', print_vars=True, sheetname='mapping_2var', header=2)

#%% TESTING 3_VARIABLES
mp = mapping_matrix(mapping_file, num_variables='three', print_vars=True, row_var3=10, sheetname='mapping_3var', header=2)


