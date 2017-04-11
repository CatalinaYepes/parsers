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
# The code provided herein is released as a prototype imappinglementation.
# It is distributed for the purpose of open collaboration and in the
# hope that it will be useful to the scientific, engineering, disaster
# risk and software design communities.
#
# The software provided herein is designed and imappinglemented
# by scientific staff. It is not developed to the design standards, nor
# subject to same level of critical review by professional software
# developers.
#
# Feedback and contribution to the software is welcome, and can be
# directed to (catalina.yepes@globalquakemodel.org).
#
# The code is therefore distributed WITHOUT ANY WARRANTY; 
# without even the imappinglied warranty of MERCHANTABILITY or 
# FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# -*- coding: utf-8 -*-

import pandas as pd

import functions
from mapping_matrix import mapping_matrix

def parse_2var_NonCrossed(data_var1, data_var2, mapping, data_type='Dwellings'):
    """Parse building data using 1 variable.
    
    :param data_vari: a DataFrame with data to use, organised as
                 - Row_1: Column headers
                 - Coulmn_1: Region_ID
                 - Column_2: Region_name
                 
    :param mapping: a :class: mapping scheme
    
    :param data_type: Header to add in the output data (Buildings, Population)
    
    :returns: DataFrame with [region_id, region_name, Taxonomy, data_type]
    """
    # Create DataFrame [id, region_name, Taxonomy, Dwellings (or Buildings)]
    info = pd.DataFrame(columns=('id', 'Region', 'Taxonomy', data_type))
    
    # Verify the variables have the same ragions:
    regions_var1 = data_var1.iloc[:,:2]
    regions_var2 = data_var2.iloc[:,:2]
    assert (pd.DataFrame.equals(regions_var1 , regions_var2) == True), 'Regions in variables are different'
    
    # Include total value of VARIABLE2 to estimate fractions
    var2_total = data_var2.iloc[:,2:].sum(axis=1)
    
    # Iterate over VARIABLE 1
    for var1 in data_var1.columns[2:]:
        if var1 in mapping.var1:
           # Iterate over VARIABLE 2
            for var2 in data_var2.columns[2:]:
                if var2 in mapping.var2:
                    print var1, var2
                    proportion = mapping.matrix.loc[var2, var1]
                    bdg_classes = functions.split_tax(proportion)
                    print bdg_classes
                    
                    for bdg_class in bdg_classes:                    
                        fraction = bdg_class[0]
                        taxonomy = pd.DataFrame({'Taxonomy': [bdg_class[1]] * len(data_var1)})
                        
                        values = data_var1[var1] * data_var2[var2] / var2_total * fraction
                        # Need to add check for NaN and '-' values
                        df = pd.concat([data_var1.iloc[:,:2], taxonomy , values], axis=1)
                        df.columns = ['id', 'Region', 'Taxonomy', data_type]
        
                        info = pd.concat([info, df], ignore_index=True)

                else:
                    raise AssertionError("Error in variable 2\n Variable '{}' not found in: \n{}".format(var2, mapping.var2))
    
        else:
            raise AssertionError("variable '{}' not found in: \n{}".format(var1, mapping.var1))
 
    # Group values
    parse_data = info.groupby(['id','Region','Taxonomy'], as_index=False).sum()

    return parse_data

data_file = 'example-data-noncrossed_variables.xlsx'
data_var1 = pd.read_excel(data_file, sheetname=0)
data_var2 = pd.read_excel(data_file, sheetname=1)
mapping = mapping_matrix(data_file, num_variables='two', sheetname='mapping_v1_v2', header=1)

test = parse_2var_NonCrossed(data_var1, data_var2, mapping)