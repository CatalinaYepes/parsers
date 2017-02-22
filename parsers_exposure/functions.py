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
Different functions for parsing an exposure model using census data.

"""
import pandas as pd

def contain(values_list, text):
    for data in values_list:
        validation = 'Incorrect'
        if str(data).find(str(text)) != -1 and pd.isnull(text) != True:        
            validation = 'Correct'
            break                     
    return validation

def split_tax(name):
    '''Function for separating the taxonomies assigned to the same mapping scheme'''
    split_name = []

    if name.find('%') != -1:
        tot = 0
        data =  name.split('\n')
        for val in data:
            value = str(val).split('% ')
            percentage = float(value[0])/100
            taxonomy = value[1]
            split_name.append([percentage, taxonomy])
            tot += percentage
    else:
        split_name.append([1.0, name])
        tot = 1
    assert (round(tot,4) == 1), "Error in the mapping scheme. Summ =! 100% \n  Review taxonomy:\n{}".format(name)
    return split_name
        
def info_append(info, values, id_region, name_region, dwellings):
    '''Function to append values into a single DataFrame '''
    if isinstance(dwellings, (str, unicode)) == True:
        dwl = 0
    else:
        for i,var in enumerate(values):
            dwl = dwellings * var[0]
            info.loc[len(info)] = [id_region, name_region, var[1], dwl]
    return info

def mapping(var1, var2, var3, mp, num_variables):
    """Function for mapping the census with the taxonomy string.
    var1: in the rows (e.g. floor material)
    var2: in the first column (e.g. wall material)
    var3: in the second column (e.g. type of dwelling)
    
    'mp' is the DataFrame that cointains the mapping scheme.
    """
    # Find the location for variable1
    col_var1 = [i for i, material in enumerate(mp.var1) if str(material).find(var1) != -1]
    
    if num_variables is not 'one':
        # Find the location for variable2
        row_var2 = [i for i, material in enumerate(mp.col0) if str(material).find(var2) != -1]        
        # Find the initial taxonomy classification
        tax1 = mp.iloc[row_var2[0],col_var1[0]]
    else:
        tax1 = mp.iloc[-1,col_var1[0]]

    assert (tax1 != []), 'Error, Taxonomy empty'
    taxo = split_tax(tax1)
    
    if num_variables == 'three':         
        # Separate tax1 -->  if it has different taxonomies, and assign percentages
        if (tax1.find('%') != -1) or (tax1.find('-') != -1):
            taxo = split_tax(tax1)
        else: 
            # Find the index for variable3
            row_var3 = [i for i, material in enumerate(mp.col0) if str(material).find(var3) != -1]
            assert (row_var3 != []), 'It was not possible to find a match btw variable3 and mapping'
            # Find the index for the 2nd mapping
            col_2mapping = [i for i, tax in enumerate(mp.second_mapping) if str(tax).find(tax1) != -1]
            assert (col_2mapping != []), 'It was not possible to find a match with the second mapping'
            
            tax2 = mp.iloc[row_var3[0],col_2mapping[0]]
            taxo = split_tax(tax2)  
    assert (taxo != []), 'The taxonomy is empty. Review material'
    return taxo

def mkdir_p(path):
    """Create a directory if it doesn't exist yet """
    import os
    import errno
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def clearall():
    all = [var for var in globals() if var[0] != "_"]
    for var in all:
        del globals()[var]
