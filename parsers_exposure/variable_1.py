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

from parsers_exposure.functions import split_tax


def parse_1var(data, mapping):
    """
    Parse building data using ONE variable.
    
    :param data: a DataFrame with data to use, organised as
                 - Row_1: Column headers
                 - Coulmn_1: Region_ID
                 - Column_2: Region_name
                 
    :param mapping: a :class: mapping scheme
    
    :returns: DataFrame with [region_id, region_name, Taxonomy, 'Dwellings']
    """
    info = pd.DataFrame(columns=('id', 'Region', 'Taxonomy', 'Dwellings'))

    # Iterate over VARIABLE 1
    for var1 in data.columns[2:]:
        if var1 in mapping.var1:
            proportion = mapping.matrix[var1][0]
            bdg_classes = split_tax(proportion)
            # print bdg_classes
            
            for bdg_class in bdg_classes:
                dwellings = pd.to_numeric(data[var1], errors='coerce')
                # Check for 'nan' or '-' values           
                if isinstance(dwellings, (str, bytes)) == True:
                    continue

                fraction = bdg_class[0]
                taxonomy = pd.DataFrame({'Taxonomy': [bdg_class[1]] * len(data)})
                
                values = dwellings * fraction
                df = pd.concat([data.iloc[:,:2], taxonomy , values], axis=1)
                df.columns = ['id', 'Region', 'Taxonomy', 'Dwellings']        
                info = pd.concat([info, df], ignore_index=True) 
        elif var1.find('Total') != -1:
            break
        else:
            raise AssertionError('variable "%s", not found in mapping_matrix' % var1)

    parse_data = info.groupby(['id','Region','Taxonomy'], as_index=False).sum()

    return parse_data

