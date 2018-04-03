# LICENSE
# Copyright (c) 2015, GEM Foundation, C. Yepes-Estrada
#
# The set of code is free software: you can redistribute
# it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with OpenQuake. If not, see <http://www.gnu.org/licenses/>
#
# DISCLAIMER
# The code provided herein is released as a prototype implementation.
# It is distributed for the purpose of open collaboration and in the
# hope that it will be useful to the scientific, engineering, disaster
# risk and software design communities.
#
# The software provided herein is designed and implemented
# by scientific staff. It is not developed to the design standards, nor
# subject to same level of critical review by professional software
# developers.
#
# Feedback and contribution to the software is welcome, and can be
# directed to (catalina.yepes@globalquakemodel.org).
#
# The code is therefore distributed WITHOUT ANY WARRANTY; 
# without even the implied warranty of MERCHANTABILITY or 
# FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# -*- coding: utf-8 -*-
"""
Parse dwellings or buildings (NON-crossed variables) based mapping schemes.

Make sure the data is stored in an excel file (.xlsx) with at least:
 i)  A sheet with data for a given variable (one variable)
 ii) Sheet with mapping schemes to cross the variables
      NOTE: The maping variables must perfectly match the data variables.
      Check the exmaple data given in "example-data-noncrossed_variables.xlsx"
      
The user can parse information based on one, two or three variables: 
  var1: in the rows (e.g. floor material)
  var2: in the first column (e.g. wall material)
  var3: in the second column (e.g. type of dwelling)
    
"""
import os
import pandas as pd

from mapping import mapping_matrix
from get_values import parse_data
from get_values import reshape_expo_data


folder = os.chdir('/Users/catalinayepes/python_code/parsers_exposure')

data_file = 'ex_data-noncrossed.xlsx'

#%% 1 VARIABLE
num_variables = 'one'
mapping = mapping_matrix(data_file, num_variables, sheetname='mapping_1v', header=1)
data = pd.read_excel(data_file, sheetname='variable_1')
save_as = 'test/example_1var'
res_1v = parse_data(data, num_variables, mapping, save_as, cross_vars=True)


#%% 2 NON-CROSSED VARIABLES
num_variables = 'two'
mapping = mapping_matrix(data_file, num_variables, sheetname='mapping_1v_2v', header=1)
data_var1 = pd.read_excel(data_file, sheetname='variable_1')
data_var2 = pd.read_excel(data_file, sheetname='variable_2')
save_as = 'test/example_2vars-noncrossed'
res_2v = parse_data([data_var1, data_var2], num_variables, mapping, save_as, cross_vars=False)

# If combining with extra NON-crossed variables
data_vars1_2 = reshape_expo_data(res_2v, save_as='test/vars1_2')
data_var3 = pd.read_excel(data_file, sheetname='variable_3')
mapping_2 = mapping_matrix(data_file, num_variables, sheetname='mapping_1v_2v_3v', header=1)
save_as = 'test/example_3vars-noncrossed'
output = parse_data([data_vars1_2, data_var3], num_variables, mapping_2, save_as, cross_vars=False)


#%% 2 CROSSED VARIABLES
num_variables = 'two'
data_file = 'ex_data-crossed.xlsx'
data = pd.read_excel(data_file, sheetname='data_2vars')
mapping = mapping_matrix(data_file, num_variables='two', sheetname='mapping_2var', header=2)
save_as = 'test/example_2vars-crossed'
res_2v = parse_data(data, num_variables, mapping, save_as, cross_vars=True)


#%% 3 CROSSED VARIABLES
num_variables = 'three'
data_file = 'ex_data-crossed.xlsx'
data = pd.read_excel(data_file, sheetname='data_3vars')
mapping = mapping_matrix(data_file, num_variables='three', row_var3=9, sheetname='mapping_3var', header=2)
save_as = 'test/example_3vars-crossed'
res_3v = parse_data(data, num_variables, mapping, save_as, cross_vars=True)


