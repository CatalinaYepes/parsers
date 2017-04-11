# -*- coding: utf-8 -*-
"""
Module :mod:`openquake.hazardlib.geo.mesh` defines classes :class:`Mesh` and
its subclass :class:`RectangularMesh`.
"""
import numpy

mesh_dt = numpy.dtype([('lon', float), ('lat', float), ('depth', float)])


def build_array(lons_lats_depths):
    """
    Convert a list of n triples into a composite numpy array with fields
    lon, lat, depth and shape (n,) + lons.shape.
    """
    shape = (len(lons_lats_depths),) + lons_lats_depths[0][0].shape
    arr = numpy.zeros(shape, mesh_dt)
    for i, (lons, lats, depths) in enumerate(lons_lats_depths):
        arr['lon'][i] = lons
        arr['lat'][i] = lats
        arr['depth'][i] = depths
    return arr