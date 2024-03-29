#!/usr/bin/env python3

import unittest
from fractions import Fraction
from planegeometry.structures.points import Point
from planegeometry.structures.polygons import Polygon
from planegeometry.triangulations.fanpm import FanTriangulationPM as Triangulation

#     4
#  5     3   najprostszy przypadek
# 6       2
#  7     1
#     0
class TestTriangulation1(unittest.TestCase):

    def setUp(self):
        # Orientacja +1.
        point_list = [Point(3, 0), Point(5, 1), Point(6, 3), Point(5, 5),
            Point(3, 6), Point(1, 5), Point(0, 3), Point(1, 1)]
        self.polygon = Polygon(*point_list)

    def test_triangulation(self):
        #print("almost circle n=8 ...")
        algorithm = Triangulation(self.polygon)
        algorithm.run()
        self.assertEqual(len(algorithm.planar_map.face2edge),
                         len(self.polygon.point_list)-1)

    def test_single_triangle(self):
        #print("single triangle ...")
        polygon = Polygon(0, 0, 1, 0, 0, 1)
        algorithm = Triangulation(polygon)
        algorithm.run()
        self.assertEqual(len(algorithm.planar_map.face2edge), 2)

    def test_square(self):
        #print("square ...")
        polygon = Polygon(0, 0, 1, 0, 1, 1, 0, 1)
        algorithm = Triangulation(polygon)
        algorithm.run()
        self.assertEqual(len(algorithm.planar_map.face2edge), 3)

    def test_collinear(self):
        polygon = Polygon(0, 0, 1, 1, 2, 2, 3, 3)
        algorithm = Triangulation(polygon)
        # Wykryje brak zakretu.
        self.assertRaises(Exception, algorithm.run)

    def tearDown(self): pass

#  9  8  7  6   wielokat wypukly z degeneracja
# 10        5
# 11        4
#  0  1  2  3
class TestTriangulation2(unittest.TestCase):

    def setUp(self):
        # Orientacja +1.
        point_list = [Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0),
            Point(3, 1), Point(3, 2), Point(3, 3), Point(2, 3),
            Point(1, 3), Point(0, 3), Point(0, 2), Point(0, 1)]
        self.polygon = Polygon(*point_list)

    def test_triangulation(self):
        #print("rectangle n=12 ...")
        algorithm = Triangulation(self.polygon)
        algorithm.run()
        self.assertEqual(len(algorithm.planar_map.face2edge),
                         len(self.polygon.point_list)-1)

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
