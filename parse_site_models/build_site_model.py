"""
Given a list of sites or asset locations, and another list of
points at which Vs30 values have been measured / inferred,
extract Vs30 values from the points closest to the input sites

@author: anirudh.rao
"""

import numpy as np
import pandas as pd
from scipy.spatial import KDTree
from tqdm import tqdm
import sys
sys.setrecursionlimit(10000)


def _calculate_z1p0(vs30):
    """
    Reads an array of Vs30 values (in m/s) and
    returns the depth to the 1.0 km/s velocity horizon (in m)

    :param vs30: the shear wave velocity (in m/s) at a depth of 30m
    """
    c1 = 6.745
    c2 = 1.35
    c3 = 5.394
    c4 = 4.48
    Z1Pt0 = np.zeros_like(vs30)
    Z1Pt0[vs30 < 180] = np.exp(c1)
    idx = (vs30 >= 180) & (vs30 <= 500)
    Z1Pt0[idx] = np.exp(c1 - c2 * np.log(vs30[idx] / 180.0))
    idx = vs30 > 500
    Z1Pt0[idx] = np.exp(c3 - c4 * np.log(vs30[idx] / 500.0))
    return Z1Pt0


def _calculate_z2p5(z1pt0):
    """
    Reads an array of z1.0 values (in m) and
    returns the depth to the 2.5 km/s velocity horizon (in km)
    Ref: Campbell, KW and Bozorgnia Y. PEER 2007/02 - "Campbell-Bozorgnia
    NGA Ground Motion Relations for the Geometric Mean
    Horizontal Component of Peak and Spectral Ground Motion Parameters"

    :param z1pt0: the depth to the 1.0 km/s velocity horizon (in m)
    """
    c1 = 0.519
    c2 = 3.595
    Z2Pt5 = c1 + z1pt0/1000. * c2
    return Z2Pt5


def _calculate_z2p5_ngaw2(vs30):
    """
    Reads an array of Vs30 values (in m/s) and
    returns the depth to the 2.5 km/s velocity horizon (in km)
    Ref: Campbell, K.W. & Bozorgnia, Y., 2014.
    "NGA-West2 ground motion model for the average horizontal components of
    PGA, PGV, and 5pct damped linear acceleration response spectra."
    Earthquake Spectra, 30(3), pp.1087–1114.

    :param vs30: the shear wave velocity (in m/s) at a depth of 30 m
    """
    c1 = 7.089
    c2 = -1.144
    Z2Pt5 = np.exp(c1 + np.log(vs30) * c2)
    return Z2Pt5


def write_site_model_file(vs30_file, sites_file, sitemodel_file):
    """
    Reads a Vs30 xyz/csv file and the sites csv file,
    and writes a site model csv file 

    :param vs30_file: path to the Vs30 xyz/csv file
    :param sites_file: path to the sites csv file (lon,lat)
    :param sitemodel_file: path to the output site model csv file
    """

    vs30_df = pd.read_csv(vs30_file, header=None, names=["LON", "LAT", "VS30"])
    points_vs30 = np.asfarray(zip(vs30_df["LON"], vs30_df["LAT"]))
    tree = KDTree(points_vs30)

    sites_df = pd.read_csv(sites_file, header=None, names=["LON", "LAT"])
    points_sites = np.asfarray(zip(sites_df["LON"], sites_df["LAT"]))

    sites_df["VS30"] = vs30_df["VS30"][tree.query(points_sites)[1]].values
    sites_df["VS30TYPE"] = "inferred"
    sites_df["Z1PT0"] = _calculate_z1p0(sites_df["VS30"].values)
    sites_df["Z2PT5"] = _calculate_z2p5_ngaw2(sites_df["VS30"].values)
    sites_df.to_csv(
        sitemodel_file,
        columns=["LON", "LAT", "VS30", "VS30TYPE", "Z1PT0", "Z2PT5"],
        header=False, index=False)