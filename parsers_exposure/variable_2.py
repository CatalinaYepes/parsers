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

def parse_2var_NonCrossed(data_var1, data_var2, mapping):
    """
    Parse building data using 2 NON-CROSSED variables.
    
    :param data_var_i: a DataFrame with data to use, organised as
                 - Row_1: Column headers
                 - Coulmn_1: Region_id
                 - Column_2: Region_name
                 
    :param mapping: a :class: mapping scheme
        
    :returns: DataFrame with [region_id, region_name, Taxonomy, Dwellings]
    """

    info = pd.DataFrame(columns=('id', 'Region', 'Taxonomy', 'Dwellings'))
    
    # Verify the variables have the same ragions:
    regions_var1 = data_var1.iloc[:,:2]
    regions_var2 = data_var2.iloc[:,:2]
    assert (pd.DataFrame.equals(regions_var1 , regions_var2) == True), 'Regions in variables are different'
    
    # Include total value of var2 to estimate fractions
    var2_total = data_var2.iloc[:,2:].sum(axis=1)
    
    # Iterate over VARIABLE 1
    for var1 in data_var1.columns[2:]:
        if var1 in mapping.var1:
           # Iterate over VARIABLE 2
            for var2 in data_var2.columns[2:]:
                if var2 in mapping.var2:
                    #print var1, var2
                    proportion = mapping.matrix.loc[var2, var1]
                    bdg_classes = functions.split_tax(proportion)
                    #print bdg_classes
                    
                    for bdg_class in bdg_classes:                    
                        fraction = bdg_class[0]
                        taxonomy = pd.DataFrame({'Taxonomy': [bdg_class[1]] * len(data_var1)})
                        
                        values = data_var1[var1] * data_var2[var2] / var2_total * fraction
                        # Need to add check for NaN and '-' values
                        df = pd.concat([data_var1.iloc[:,:2], taxonomy , values], axis=1)
                        df.columns = ['id', 'Region', 'Taxonomy', 'Dwellings']
        
                        info = pd.concat([info, df], ignore_index=True)

                else:
                    raise AssertionError("Error in variable 2\n Variable '{}' not found in: \n{}".format(var2, mapping.var2))
    
        else:
            raise AssertionError("variable '{}' not found in: \n{}".format(var1, mapping.var1))
 
    parse_data = info.groupby(['id','Region','Taxonomy'], as_index=False).sum()

    return parse_data


def census_2var_Crossed(data, mapping):
    """
    Parse census data using 2 CROSSED variables.
    
    :param data: a DataFrame with data to use, organised as
                 - Rows: variable 1 (e.g. floor material)
                 - Coulmns: variable 2 (e.g. wall material)
                 NOTE: The name of the region should be placed in ColumnB and
                       ColumnA should has the region ID starting with 'AREA # '

    :param mapping: a :class: mapping scheme

    :returns: DataFrame with [region_id, region_name, Taxonomy, Dwellings]
    """
    
    # Rename columns to work faster using mapping variables
    col_names = list(mapping.var1)
    col_names.insert(0, 'variable_2')
    data.rename(columns={list(data)[x]:name for x, name in enumerate(col_names)}, inplace = True)
    
    info = []
   
    # Set default values
    region_name = 'National'
    region_id = 'AREA # 00'
    
    # Iterate over VARIABLE 2
    for row_var2, var2 in enumerate(data.variable_2):
        # Identify the region
        if str(var2).find('AREA') != -1:
            region_name = data.iloc[row_var2, 1]
            region_id = data.variable_2[row_var2]
            print 'Region: {}, {}'.format(region_id, region_name)
            continue
        elif var2 == 'RESUMEN' or var2 == 'SUMMARY':
            region_name = 'SUMMARY'
            continue  # We can't use `break` because some data has summary for each region
        
        if var2 in mapping.var2 and (region_name != 'SUMMARY'):
            #print row_var2, "-->", var2
         
            # Iterate over VARIABLE 1
            for var1 in mapping.var1:
                if  var1 == 'Total':
                    #print '''--- End of the variable1'''
                    break
                #print var1, '-->', var1
                
                dwellings = data[var1][row_var2]
                #print ('''There are {} dwellings with:\n  var1: {}\n  var2: {}''').format(dwellings, var1, var2)                
                # Check for 'nan' or '-' values           
                if isinstance(dwellings, (str, unicode)) == True:
                    continue
                
                proportion = mapping.matrix.loc[var2, var1]
                bdg_classes = functions.split_tax(proportion)

                for bdg_class in bdg_classes:                    
                    fraction = bdg_class[0]
                    taxonomy = bdg_class[1]
                    
                    values = dwellings * fraction
                    info.append([region_id, region_name, taxonomy , values])
    
        elif var2 == 'Total':
            #print '---End of the region {} ---'.format(region_name)
            continue
        elif var2 == 'RESUMEN' or var2 == 'SUMMARY':
            #print '-----END-----'
            break
        else:
            #print '.'
            continue  
    
    info = pd.DataFrame(info, columns=('id', 'Region', 'Taxonomy', 'Dwellings'))
    parse_data = info.groupby(['id','Region','Taxonomy'], as_index=False).sum()
    
    return parse_data