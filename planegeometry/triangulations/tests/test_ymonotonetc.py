#!/usr/bin/python3

import unittest
from fractions import Fraction
from planegeometry.structures.points import Point
from planegeometry.structures.polygons import Polygon
from planegeometry.triangulations.ymonotonetc import YMonotoneTriangulationTC as Triangulation

#     4
# 5       3
#   6   2
# 7       1
#     0
class TestTriangulation1(unittest.TestCase):

    def setUp(self):
        # Orientacja +1.
        point_list = [Point(2, 0), Point(4, 1), Point(3, 3), Point(4, 4),
            Point(2, 5), Point(0, 4), Point(1, 3), Point(0, 1)]
        self.polygon = Polygon(*point_list)

    def test_triangulation(self):
        algorithm = Triangulation(self.polygon)
        algorithm.run()
        self.assertEqual(len(algorithm.tc), 6)
        #print ( "triangulation graph ..." )
        #G = algorithm.tc.to_graph()
        #G.show()

    def tearDown(self): pass

#   5
#     4
#         3
#         2
# 6   1
#   0
class TestTriangulation2(unittest.TestCase):

    def setUp(self):
        # Orientacja +1.
        point_list = [Point(0, 0), Point(1, 1), Point(3, 2), Point(3, 3),
            Point(1, 4), Point(0, 5), Point(1, 2)]
        self.polygon = Polygon(*point_list)

    def test_triangulation(self):
        algorithm = Triangulation(self.polygon)
        algorithm.run()
        self.assertEqual(len(algorithm.tc), 5)
        #print ( "triangulation graph ..." )
        #G = algorithm.tc.to_graph()
        #G.show()

    def tearDown(self): pass

#  8
#           7
#    9
#    10
#   11
# 12
#           6
#    5
#     4
#       3
#         2
#         1
# 0
class TestTriangulation3(unittest.TestCase):

    def setUp(self):
        # Orientacja +1.
        point_list = [Point(0, 0), Point(5, 1), Point(5, 2),
            Point(3, 3), Point(2, 4), Point(1, 6), Point(5, 7),
            Point(4, 12), Point(2, 13), Point(3, 11), Point(3, 10),
            Point(2, 9), Point(0, 8)]
        self.polygon = Polygon(*point_list)

    def test_triangulation(self):
        algorithm = Triangulation(self.polygon)
        algorithm.run()
        self.assertEqual(len(algorithm.tc), 11)
        #print ( "triangulation graph ..." )
        #G = algorithm.tc.to_graph()
        #G.show()

    def tearDown(self): pass
#    9
#        8   7
#        5   6+
# 10     4   3
#        1   2+   z plusem podwyzszone
#    0
class TestTriangulation4(unittest.TestCase):

    def setUp(self):
        # Orientacja +1.
        point_list = [Point(1, 0), Point(2, 1), Point(3, 1.1),
            Point(3, 2), Point(2, 2), Point(2, 3), Point(3, 3.1),
            Point(3, 4), Point(2, 4), Point(1, 5), Point(0, 2)]
        self.polygon = Polygon(*point_list)

    def test_triangulation(self):
        algorithm = Triangulation(self.polygon)
        algorithm.run()
        self.assertEqual(len(algorithm.tc), 9)
        #print ( "triangulation graph ..." )
        #G = algorithm.tc.to_graph()
        #G.show()

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
