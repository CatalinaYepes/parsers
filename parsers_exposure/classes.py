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
Classes for parsing an exposure model using census data

"""

import pandas as pd
import parse_census
import functions
import sys    # sys.setdefaultencoding is cancelled by site.py
reload(sys)    # to re-enable sys.setdefaultencoding()
sys.setdefaultencoding('utf-8')

class ReadCensus:
    '''Parse census data into dwelling fractions using a 'Mapping scheme'.
    The user can parse information based on one, two or three variables: 
    var1: in the rows (e.g. floor material)
    var2: in the first column (e.g. wall material)
    var3: in the second column (e.g. type of dwelling)
    '''
    def __init__(self, name, file_location, num_var):
        print ('\n... parsing {} ...').format(name.capitalize())
        self.name = name
        self.file_name = file_location
        self.file = pd.ExcelFile(file_location)
        self.num_variables = num_var
        
            
    def mapping_matrix(self, mapping_sheet='Mapping', row_var1=None, row_var3=None, print_vars=False):
        ''' Read and parse MAPPING MATRIX 
            row_var1: Row index for variable 1 in the mapping scheme (starting in zero)
            row_var3: Row index for variable 3 in the mapping scheme (starting in zero)
            '''
        self.mp = self.file.parse(sheetname=mapping_sheet)
        self.mp.columns = range(len(self.mp.columns))
        self.mp.var1 = self.mp.iloc[row_var1 - 1]
        self.mp.col0 = self.mp[0]
        if self.num_variables == 'three':
            self.mp.var2 = self.mp[0][: row_var3 - 1]
            self.mp.var3 = self.mp[0][row_var3 : ]
            self.mp.second_mapping = self.mp.iloc[row_var3 - 1] 
            if print_vars == True:
                print '''\n   ---   Var1 =   ---   \n\n{}
                \n   ---   Var2 =   ---   \n\n{}
                \n   ---   Var3 =   ---   \n\n{}'''.format(self.mp.var1, self.mp.var2, self.mp.var3)
        elif self.num_variables == 'two':
            self.mp.var2 = self.mp[row_var1 : ][0]
            if print_vars == True:
                print '''\n   ---   Var1 =   ---   \n\n{}
                \n   ---   Var2 =   ---   \n\n{}'''.format(self.mp.var1, self.mp.var2)
        elif self.num_variables == 'one':
            if print_vars == True:
                print '''\n   ---   Var1 =   ---   \n\n{}'''.format(self.mp.var1)
                   
    def parse_info(self, parse_sheet, admin_level=None, save_folder_name=None, save_regions=False, save_data=False):
        '''parsing data from census
        several variables available:
            parse_sheet:      Name or number of the sheet to parse [mandatory]
                              (NOTE: number of the sheets start from 0)
            admin_level:      Number/Name to add to all saved data (default=parse_sheet) [optional]
            save_folder_name: Folder name to save data (default None) [optional]
            save_regions:     True or False for aggregating data into regions (default False)
            save_data:        True or False (default False)
        '''
        if isinstance( parse_sheet, int ):
            print ('''\n parsing sheet [{}], sheet_name: {}\n''').format(parse_sheet, self.file.sheet_names[parse_sheet])
        else:
            print ('''\n parsing sheet_name: {}\n''').format(parse_sheet)
                
        
        if admin_level is not None:
            self.level = admin_level
        else:
            self.level = parse_sheet
        sheet = self.file.parse(sheetname=parse_sheet)
        
        if self.num_variables == 'three':
            sheet.columns = range(len(sheet.columns))
            info = parse_census.census_3var(sheet, self.mp)
        elif self.num_variables == 'two':
            sheet.columns = range(len(sheet.columns))
            info = parse_census.census_2var(sheet, self.mp)
        elif self.num_variables == 'one':
            info = parse_census.census_1var(sheet, self.mp)    
                
        dwellings = info.groupby(['id','Region','Taxonomy'], as_index=False).sum() 
        self.dwellings = dwellings
        print ('''\nDwelling information for {}, sheet_name {} has been stored.
                Total dwellings  =  {}''').format(self.name, parse_sheet, float(dwellings.Dwellings.sum()))
        
        if save_data == True:
            print '\n saving data in csv \n'
            save_dwellings_csv(self, dwellings, save_folder_name, save_regions)
        
        return dwellings
        
def save_dwellings_csv(self, dwellings, save_folder_name, save_regions):
    '''Save dwellings in csv format'''    
    if isinstance(save_folder_name, str):
        self.folder = save_folder_name
    else:
        if isinstance(self.level, str):
            self.folder = self.level
        else:
            self.folder = 'level_'.format(self.level)    
    functions.mkdir_p(self.folder)
    
    save_as = ('{}/{}-{}').format(self.folder, self.name, self.level)       
    
    dwellings.Dwellings = dwellings.Dwellings.round(1)
    dwellings.to_csv(save_as + '-dwelings.csv', index=False)
    
    if save_regions == True:
        regions = dwellings[['id','Region','Taxonomy','Dwellings']]
        regions = regions.groupby(['id','Region']).sum() 
        regions.Dwellings = regions.Dwellings.round(1)
        regions.to_csv(save_as + '-regions.csv')        
    
    print '''----- end -----
    '''
