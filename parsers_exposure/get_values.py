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
#import sys    # sys.setdefaultencoding is cancelled by site.py
#reload(sys)    # to re-enable sys.setdefaultencoding()
#sys.setdefaultencoding('utf-8')

from parsers_exposure.variable_1 import parse_1var
from parsers_exposure.variable_3 import census_3var_Crossed
from parsers_exposure import variable_2


def parse_data(data, num_variables, mapping, save_as=None, cross_vars=True):
    '''parsing data from census
    several variables available:
        parse_sheet:      Name or number of the sheet to parse [mandatory]
                          (NOTE: number of the sheets start from 0)
        admin_level:      Number/Name to add to all saved data (default=parse_sheet) [optional]
        save_folder_name: Folder name to save data (default None) [optional]
        save_regions:     True or False for aggregating data into regions (default False)
        save_data:        True or False (default False)
    
    : returns info: DataFrame [id, Region, Taxonomy, Dwellings (or Buildings)]
    '''
    print ('\nParsing data for %s \n' % save_as)
    
    if num_variables == 'one':
        print ('\n Parsing 1 VARIABLE data \n')
        info = parse_1var(data, mapping)

    elif num_variables == 'two':
        if cross_vars == True:
            print ('\n Parsing 2 CROSSED VARIABLES data \n')
            info = variable_2.census_2var_Crossed(data, mapping)            
        else:
            assert (isinstance(data, list) and len(data) == 2), 'using NON-CROSSED-VARIABLES, data must be a list of two DataFrames'
            print ('\n Parsing 2 NON-CROSSED VARIABLES data \n')
            info = variable_2.parse_2var_NonCrossed(data[0], data[1], mapping)

    elif num_variables == 'three':
        if cross_vars == True:
            print ('\n Parsing 3 CROSSED VARIABLES data \n')
            info = census_3var_Crossed(data, mapping)
        else:
            raise AssertionError('3 variables must be CROSSED')

    assert (info.empty == False), 'Empty DataFrame'
    
    tot_census_dwl = info.iloc[:,3].sum()
    print ('Total census dwellings: %s' % tot_census_dwl)
    # # Round Dwellings/Buildings to 2 decimal places
    # info.iloc[:,3] = info.iloc[:,3].round(2)
    # # Save exposure oly for Dwellings >= 0.5    
    # info = info[info.iloc[:,3] >= 0.5]
    #tot_exposure_dwl = info.iloc[:,3].sum()   
    #print ('''
    #    Total census dwellings:  {}
    #    Total exposure dwellings: {}
    #    Difference: {}%'''.format(tot_census_dwl, tot_exposure_dwl, round(tot_exposure_dwl / tot_census_dwl, 1)))
    
    if save_as:
        info.to_csv(save_as + '.csv', index=False, encoding='utf-8')
        print ('''Data saved in:
                 %s.csv''' % save_as)

    return info


def reshape_expo_data(data, save_as=None):
    '''
    Reshape resulting exposure data to convert it as 1var_data
    
    :param data: Dataframe with columns:
                 ['id', 'Region', 'Taxonomy', 'Dwellings']
    
    :param save_as: save reshaped data in file
    '''    
    rs_data = data.pivot_table(index=['id', 'Region'], columns='Taxonomy', values='Dwellings')
    rs_data.reset_index(inplace=True)
    
    if save_as == None:
        print ('\n Data reshaped but not saved')
    else:
        rs_data.to_csv(save_as + '.csv', index=False, encoding='utf-8')
        print ('\n Reshaped data saved in %s' % save_as)
    
    return rs_data
    
        