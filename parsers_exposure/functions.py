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

def split_tax(name):
    '''Function for separating the taxonomies assigned to the same mapping scheme'''
    split_name = []

    if name.find('%') != -1:
        tot = 0
        data =  name.split('\n')
        for val in data:
            if not val == '':
                value = str(val).split('% ')
                percentage = float(value[0])/100
                taxonomy = value[1]
                split_name.append([percentage, taxonomy])
                tot += percentage
    else:
        split_name.append([1.0, name])
        tot = 1
    assert (round(tot,4) == 1), "Error in the mapping scheme. Summ =! 100% \n  Review taxonomy:\n{}".format(name)
    assert (split_name != []), 'Error, Taxonomy empty'    
    return split_name


def check_DataFrame(data):
    '''Check that `VARIABLE 2` is not in the index of the DF'''
    if not data.index.is_monotonic:
        data.reset_index(inplace=True)
        print 'Reset Index in DataFrame'
    
    return data


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