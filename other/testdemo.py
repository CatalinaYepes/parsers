import unittest
import numpy as np

from openquake.hazardlib.geo.line import Line
from openquake.hazardlib.geo.point import Point

from dpp.dpplib import get_xyz_from_ll
from dpp.dpplib import projection_pp
from dpp.dpplib import define_hypocentre_patch_index


class CoordinateConversionTest(unittest.TestCase):

    def test_get_xyz_from_ll(self):

        projected = Point(5., 6., 0.)
        reference = Point(4., 6., 0.)
        xs, ys, zs = get_xyz_from_ll(projected, reference)
        # The value used for this test is computed using this website
        # http://www.movable-type.co.uk/scripts/latlong.html
        self.assertAlmostEqual(xs, 111.2, delta=2.0)
        self.assertAlmostEqual(ys, 0.1, delta=2.0)
        self.assertAlmostEqual(zs, 0.0, delta=2.0)


class ProjectionPpTest(unittest.TestCase):

    def test_projectionpp(self):

        site = Point(1., 0.5, 1.)
        normal = np.array([3., -2., 1.])
        dist_to_plane = 2.
        hypo = Point(0, 0, 0)
        pp = projection_pp(site, normal, dist_to_plane, hypo)
        # The value used for this test is computed using this website
        # http://www.nabla.hr/CG-LinesPlanesIn3DB5.htm#Projection
        self.assertAlmostEqual(pp[0], 64.19, delta=0.1)
        self.assertAlmostEqual(pp[1], 86.94, delta=0.1)
        self.assertAlmostEqual(pp[2], -16.67, delta=0.1)


class PatchIndexTest(unittest.TestCase):

    def test_hypocentre_index(self):
        hypocentre = Point(1., 0., 3.)
        fault_trace = Line([Point(0., 0., 0.), Point(2., 0., 0.),
                           Point(4., 4., 4.)])
        upper_seismogenic_depth = 0.
        lower_seismogenic_depth = 5.
        dip = 90.
        index = define_hypocentre_patch_index(hypocentre,
                                              fault_trace,
                                              upper_seismogenic_depth,
                                              lower_seismogenic_depth,
                                              dip)
        # The value used for this test is computed using this website
        # http://www.vitutor.com/geometry/vec/angle_vectors.html
        # we take the value and convert to radian.
        self.assertEqual(index, 1)
