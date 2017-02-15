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

import pandas as pd
import functions

def census_3var(sheet, mp):
    """Parse census data using 3 variables.
    The DataFrame should be organised with:
    var1: in the rows (e.g. floor material)
    var2: in the first column [columnA] (e.g. wall material)
    var3: in the second column [columnB] (e.g. type of dwelling)
    
    The name of the region should be placed in ColumnB and
    ColumnA should contain the region ID starting with 'AREA # '
    """
    col0 = sheet[0] #column with VARIABLE_2
    col1 = sheet[1] #column with VARIABLE_3
    
    # Create a DataFrame with [id, name_region, Taxonomy, # of dwellings]
    info = pd.DataFrame(columns=('id', 'Region', 'Taxonomy', 'Dwellings'))
    name_region = 'Nacional'
    id_region = 'AREA # 00'
    
    for row_var2, variable2 in enumerate(col0):    
        # Identify the region
        if str(variable2).find('AREA') != -1:
            name_region = col1[row_var2]
            id_region = col0[row_var2]
            print "Region ", id_region, " --> ", name_region
            continue
        elif variable2 == 'RESUMEN':
            name_region = 'RESUMEN'
            continue
        
        # Check if the variable2 is present in the mapping scheme
        if (functions.contain(mp.var2, variable2) == 'Correct') & (name_region != 'RESUMEN'):
#            print row_var2, "-->", variable2
         
            # Iterate over variable1 (rows, e.g. floor material)
            for column in range(2,len(sheet.columns)):
                variable1 = sheet.iloc[row_var2, column]
                if  variable1 == 'Total':
#                    print '''--- End of the variable1'''
                    break
#                print column, '-->', variable1
                
                # Iterate over variable3 (2nd column, e.g. house type)
                i = 1
                while True:
                    variable3 = col1[row_var2 + i]
#                    print str(row_var2 + i),'-->', variable3
                    if variable3.find('Total') != -1:
#                        print '''--- End of the variable3'''
                        break
                    else:
                        dwellings = sheet.iloc[row_var2 + i, column]
#                        print ('''There are {} dwellings with:
#                        var1: {}
#                        var2: {}
#                        var3: {}''').format(dwellings, variable1, variable2, variable3)  
                        values = functions.mapping(variable1, variable2, variable3, mp, num_variables='three')
                        info = functions.info_append(info, values, id_region, name_region, dwellings)
                        i += 1
#                        print values
#                        print info
        elif variable2 == 'Total':
#            print '---End of the region {} ---'.format(name_region)
            continue
        else:
#            print '.'
            continue  

    return info
    
def census_2var(sheet,mp):
    """Parse census data using 2 variables.
    The DataFrame should be organised with:
    var1: in the rows (e.g. floor material)
    var2: in the column [columnA] (e.g. wall material)
    
    The name of the region should be placed in ColumnB and
    ColumnA should contain the region ID starting with 'AREA # '.
    """
    col0 = sheet[0] #column with VARIABLE_2

    # Create a DataFrame with [id, name_region, Taxonomy, # of dwellings]
    info = pd.DataFrame(columns=('id', 'Region', 'Taxonomy', 'Dwellings'))
    name_region = 'Nacional'
    id_region = 'AREA # 00'
    
    for row_var2, variable2 in enumerate(col0):

        # Identify the region
        if str(variable2).find('AREA') != -1:
            name_region = sheet.iloc[row_var2, 1]
            id_region = col0[row_var2]
            print "Region ", id_region, " --> ", name_region
            continue
        
        # Check if the variable2 is present in the mapping scheme
        if (functions.contain(mp.var2, variable2) == 'Correct') & (name_region != 'RESUMEN'):
#            print row_var2, "-->", variable2
         
            # Iterate over the possible variable1
            for column in range(1,len(sheet.columns) - 1): #to delete the last column with 'total'to match mp.var1
                variable1 = mp.var1[column]
                if  variable1 == 'Total':
#                    print '''--- End of the variable1'''
                    break
#                print column, '-->', variable1
                
                dwellings = sheet.iloc[row_var2, column]
#                print ('''There are {} dwellings with:
#                        var1: {}
#                        var2: {}''').format(dwellings,variable1, variable2)  
                values = functions.mapping(variable1, variable2, '', mp, num_variables='two')
                info = functions.info_append(info, values, id_region, name_region, dwellings)
#                print values
#                print info
        elif variable2 == 'Total':
#            print '---End of the region {} ---'.format(name_region)
            continue
        elif variable2 == 'RESUMEN':
#            print '-----END-----'
            break
        else:
#            print '.'
            continue  

    return info

def census_1var(sheet,mp):
    """Parse census data using 1 variable. The DataFrame should be organised with:        
        FIRST ROW: should have the variable to classify dwellings
        ColumnA should contain the region ID
        ColumnB should contain the name of the region
    """
    # Create a DataFrame with [id, name_region, Taxonomy, # of dwellings]
    info = pd.DataFrame(columns=('id', 'Region', 'Taxonomy', 'Dwellings'))
    
    # Iterate over first column (ragion_name)
    for row in range(len(sheet)):
        id_region = sheet.iloc[row][0]
        name_region = sheet.iloc[row][1]
        print 'Region ', id_region, " --> ", name_region
        # Iterate over the row variables
        for col, var in enumerate(sheet.columns[2:]):
            # Check if the variable is present in the mapping scheme
            if (functions.contain(mp.var1, var) == 'Correct'):
                dwellings = sheet[var][row]
#                print ('''   {} dwellings with {}''').format(dwellings, var)
                
                values = functions.mapping(var, '', '', mp, num_variables='one')
                info = functions.info_append(info, values, id_region, name_region, dwellings)

            elif var == 'Total':
                print '---End of the region {} ---'.format(name_region)
                continue
            else:
                print '.'
                continue  

    return info