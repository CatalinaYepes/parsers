# -*- coding: utf-8 -*-
"""
    Find a collection of code, links and other useful GIS stuff at:
     *  http://pygis.blogspot.it/2012/10/pyshp-attribute-types-and-point-files.html

    **  Useful info for storing geodata data as attributes:
        C is ASCII characters (text, string).
            w.field('taxonomy', 'C', 100)
        N is a double precision integer limited to around 18 characters in length
            w.field('id', 'N', 11, 0) # 32-bit long int
        F is for floating point numbers with the same length limits as N
        D is for dates in the YYYYMMDD format, with no spaces or hyphens between the sections
        L is for logical data (boolean). The values it can receive are 1, 0, y, n, Y, N, T, F, True and False
"""

import sys    # sys.setdefaultencoding is cancelled by site.py
import shapefile
import pandas as pd

reload(sys)    # to re-enable sys.setdefaultencoding()
sys.setdefaultencoding('utf-8')


def join_to_shape(shape_file, data_file, join_shape_by, join_data_by, columns=None, save_as=None):
    '''
    Input a shape_file and join columns from a data_file (*.csv). Return new shapefile.
    
    join_shape_by, join_data_by: column names to be used as a reference to join data
    **NOTE: If the data_file has duplicate rows for the column to join, return sum of data 
    
    columns: list of column headers to join with the shapefile
    **NOTE: ONLY columns with numerical values are added to the shapefile    
    '''

    #  1) Read shapefile
    #  ------------------------------------------------------------------------
    sf = shapefile.Reader(shape_file)
    
    fields = [x[0] for x in sf.fields[1:]] 
    #print '\n Shapefile columns: \n %s \n' % fields     
    shape = pd.DataFrame(sf.records(), columns=fields)
    
    
    #  2) Read data file and select columns
    #  ------------------------------------------------------------------------
    data = pd.read_csv(data_file)
    
    assert (join_data_by in data.columns), '''\n '%s' column doesn't exist in data_file''' % join_data_by 
    join_col = pd.DataFrame(data[join_data_by])
    
    if columns is not None:
        assert (columns.__class__ == list), '\n columns must be a list' 
        for col in columns:
            assert (col in data.columns), '\n the header %s doesnt exist in data_file' % col 
        data = data[columns].select_dtypes(include=['int64', 'float64']) # Only select columns with numerical values
    else:
        data = data.select_dtypes(include=['int64', 'float64'])
        
    if not join_data_by in data.columns:
        data = join_col.join(data)
    add_cols = data.drop(join_data_by, axis=1).columns    
    #print '\n Column headers in data: \n', list(data.columns)    
    

    #  3) Additional checks
    #  ------------------------------------------------------------------------
    if not data[join_data_by].dtypes == shape[join_shape_by].dtypes:
        data[join_data_by] = data[join_data_by].astype(float)
        shape[join_shape_by] = shape[join_shape_by].astype(float)
        
        assert (data[join_data_by].dtypes == shape[join_shape_by].dtypes), \
            '\n the columns to join have different types: \n join data: {} \n join shape: {}'.format(data[join_data_by].dtypes, shape[join_shape_by].dtypes)


    #  4) Join attributes
    #  ------------------------------------------------------------------------
    # sum the duplicated values for the data column to join
    group_data = data.groupby(join_data_by, as_index=False).sum()
    
    records = pd.merge(left=shape, right=group_data, how='left', left_on=join_shape_by, right_on=join_data_by)
    if join_data_by in records:
        if join_data_by != join_shape_by:
            records.drop(join_data_by, axis=1, inplace=True)
    else:
        records.drop(join_data_by + '_y', axis=1, inplace=True)
    records.fillna(0, inplace=True)

    # Raise error when columns are not properly merged
    assert (sum(records[columns[0]]) != 0), 'Error when merging data. Check the columns to merge'
    

    #  5) Create shape file with new attributes 
    #  ------------------------------------------------------------------------
    w = shapefile.Writer() # Create a new shapefile and specify additional columns
    w._shapes.extend(sf.shapes()) # Copy over the geometry without any changes
    w.fields = list(sf.fields) # Add the columns from existing shapefile 
    
    # Add new fields
    for header in add_cols:
        w.field(header,'F', 20, 8) # float    
    
    # Loop through each record and add a row
    for rec in records.values:
        w.records.append(rec)     # Add the modified record to the new shapefile
    
    # Save as a new shapefile (or write over the old one)
    if save_as == None:        
        save_as = shape_file.split('.')[0] + '_join'
    print '\n Saving shape file in %s' % save_as
    w.save(save_as) 

    return records
