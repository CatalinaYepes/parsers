# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 11:16:46 2017

@author: catalinayepes
"""

from parsers_shapefiles import join_to_shape


shape_file = 'test_join_to_shape/test_shape.shp'
data_file = 'test_join_to_shape/test_data.csv'
join_data_by = 'id_1'
join_shape_by = 'id_string' 
cols = ['Buildings', 'Tot_cost', 'Population']
output_file ='test_join_to_shape/output_shape'

join_to_shape.join_to_shape(shape_file, data_file, join_shape_by, 
                            join_data_by, columns=cols, save_as=output_file)
                     