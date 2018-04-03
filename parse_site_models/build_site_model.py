'''
Given a list of sites or asset locations, and another list of
points at which vs30 values have been measured / inferred,
extract vs30 values from the points closest to the input sites

@author: anirudh.rao
'''

import numpy as np
import pandas as pd
from scipy.spatial import KDTree
import xml.etree.ElementTree as ET
import lxml.etree as etree
import sys
sys.setrecursionlimit(10000)


def _calculate_z1p0(vs30):
    '''
    Reads an array of vs30 values (in m/s) and
    returns the depth to the 1.0 km/s velocity horizon (in m)

    :param vs30: the shear wave velocity (in m/s) at a depth of 30m
    '''
    c1 = 6.745
    c2 = 1.35
    c3 = 5.394
    c4 = 4.48
    z1pt0 = np.zeros_like(vs30)
    z1pt0[vs30 < 180] = np.exp(c1)
    idx = (vs30 >= 180) & (vs30 <= 500)
    z1pt0[idx] = np.exp(c1 - c2 * np.log(vs30[idx] / 180.0))
    idx = vs30 > 500
    z1pt0[idx] = np.exp(c3 - c4 * np.log(vs30[idx] / 500.0))
    return z1pt0


def _calculate_z2p5(z1pt0):
    '''
    Reads an array of z1.0 values (in m) and
    returns the depth to the 2.5 km/s velocity horizon (in km)
    Ref: Campbell, KW and Bozorgnia Y. PEER 2007/02 - 'Campbell-Bozorgnia
    NGA Ground Motion Relations for the Geometric Mean
    Horizontal Component of Peak and Spectral Ground Motion Parameters'

    :param z1pt0: the depth to the 1.0 km/s velocity horizon (in m)
    '''
    c1 = 0.519
    c2 = 3.595
    z2pt5 = c1 + z1pt0/1000. * c2
    return z2pt5


def _calculate_z2p5_ngaw2(vs30):
    '''
    Reads an array of vs30 values (in m/s) and
    returns the depth to the 2.5 km/s velocity horizon (in km)
    Ref: Campbell, K.W. & Bozorgnia, Y., 2014.
    'NGA-West2 ground motion model for the average horizontal components of
    PGA, PGV, and 5pct damped linear acceleration response spectra.'
    Earthquake Spectra, 30(3), pp.1087–1114.

    :param vs30: the shear wave velocity (in m/s) at a depth of 30 m
    '''
    c1 = 7.089
    c2 = -1.144
    z2pt5 = np.exp(c1 + np.log(vs30) * c2)
    return z2pt5


def write_site_model_file(vs30_df, sites_df, sitemodel_file, save_csv=False):
    '''
    Reads a vs30 DataFrame and the sites DataFrame,
    and writes a site model csv file 

    :param vs30_df: DataFrame with vs30 values columns=['lon', 'lat', 'vs30']
    :param sites_df: DataFrame with site locations columns=['lon', 'lat']
    :param sitemodel_file: path to the output site model csv file
    '''
    
    points_vs30 = np.asfarray(list(zip(vs30_df['lon'], vs30_df['lat'])))
    tree = KDTree(points_vs30)

    points_sites = np.asfarray(list(zip(sites_df['lon'], sites_df['lat'])))

    sites_df['vs30'] = vs30_df['vs30'][tree.query(points_sites)[1]].values
    sites_df['vs30type'] = 'inferred'
    sites_df['z1pt0'] = _calculate_z1p0(sites_df['vs30'].values)
    sites_df['z2pt5'] = _calculate_z2p5_ngaw2(sites_df['vs30'].values)
    
    if save_csv == True:
        sites_df.to_csv(
            sitemodel_file,
            columns=['lon', 'lat', 'vs30', 'vs30type', 'z1pt0', 'z2pt5'],
            header=True, index=False)
    return sites_df


def site_model_to_NRML(site_model, save_xml):
    '''
    Reads a site_model csv file and saves it in xml format 

    :param site_model: DataFrame with the site model file
                    cols = ['lon', 'lat', 'vs30', 'vs30type', 'z1pt0', 'z2pt5']
    :param save_as: path to the output site model xml file
    '''

    root = ET.Element('nrml')
    root.set('xmlns:gml', "http://www.opengis.net/gml")
    root.set('xmlns', "http://openquake.org/xmlns/nrml/0.4")
    root_model = ET.SubElement(root, 'siteModel')
    
    for row in site_model.values:
        value = ET.SubElement(root_model, 'site')
        value.set('lon', str(round(row[0], 6)))
        value.set('lat', str(round(row[1], 6)))
        value.set('vs30', str(row[2]))
        value.set('vs30Type', str(row[3]))
        value.set('z1pt0', str(round(row[4], 3)))
        value.set('z2pt5', str(round(row[5], 3)))

    # to save
    tree = ET.ElementTree(root)
    tree.write(save_xml)
    x = etree.parse(save_xml)    
    # print etree.tostring(x, pretty_print = True)
    
    output_file = open(save_xml, 'wb')
    output_file.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
    output_file.write(etree.tostring(x, pretty_print = True))
    output_file.close()