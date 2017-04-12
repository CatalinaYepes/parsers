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

import sys    # sys.setdefaultencoding is cancelled by site.py
import pandas as pd

reload(sys)    # to re-enable sys.setdefaultencoding()
sys.setdefaultencoding('utf-8')

class mapping_matrix:
    '''
    Read a 'Mapping scheme' for assigning building classes
    One, two or three possible variables: 
        :var1: in the rows (e.g. floor material)
        :var2: in the first column (e.g. wall material)
        :var3: in the second column (e.g. type of dwelling)    
    '''

    def __init__(self, mapping_file, num_variables='two', row_var3=None, print_vars=True, **kwds):
        '''            
        NOTE: The header of the spreadsheet must be set to get as column headers the var1.
              Use **kwds from pandas.read_excel (sheetname= and header=)

        :param num_variables: Number of variables in the mapping scheme (one, two, or three)
                
        :param row_var3: Row index for var3 in the mapping scheme (starts in zero) 
            
        :param print_vars: True or False

        :**kwds: Use keywords from pandas.read_excel
        '''
        
        self.mapping_file = mapping_file
        print '''\n mapping_matrix: {} \n'''.format(mapping_file) 
        self.matrix = pd.read_excel(mapping_file, **kwds)
        
        self.var1 = self.matrix.columns.values
        self.first_column = self.matrix.index.values
                    
        if print_vars == True:
            print '''_____ VARIABLE 1 _____\n{}'''.format(self.var1)
                
        if num_variables == 'two':
            self.var2 = self.first_column
            if print_vars == True:
                print '''\n_____ VARIABLE 2 _____\n{}'''.format(self.var2)

        if num_variables == 'three':
            assert (row_var3 != None), 'Define row_var3 (index for var3 in the mapping scheme)'
            self.var2 = self.first_column[ : row_var3]
            self.var3 = self.first_column[row_var3 : ]
            
            second_mapping = self.matrix.iloc[row_var3:,:]
            second_mapping.dropna(1, inplace=True)
            second_mapping.rename(columns=second_mapping.iloc[0], inplace=True)
            second_mapping.drop(second_mapping.index[0], inplace=True)
            
            self.second_mapping = second_mapping
            if print_vars == True:
                print '''\n_____ VARIABLE 2 _____\n{}'''.format(self.var2)
                print '''\n_____ VARIABLE 3 _____\n{}\n'''.format(self.var3)
                print '''\n_____ 2nd MAPPING _____\n{}\n'''.format(self.second_mapping.columns)
        