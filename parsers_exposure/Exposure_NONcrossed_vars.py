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
import classes

folder = os.chdir('/Users/catalinayepes/python_code/parsers_exposure')
file_location = 'example-data-noncrossed_variables.xlsx'        


nickname = 'example'  # to add to the saved file
num_var = 'two' # Number of variables in the data (small letter)
single_var = classes.ReadCensus(nickname, file_location, num_var)

mapping_sheet = 'mapping_v1_v2' # name or location of mapping matrix
single_var.mapping_matrix(mapping_sheet, row_var1=1, print_vars=True)

#parse_sheet = 'example_1var' # name or location of sheet to parse (example: 0 or 'Sheet1')
#save_folder_name = 'example_1var' #folder name to save parsed data
#single_var.parse_info(parse_sheet, save_regions=False, save_data=True)