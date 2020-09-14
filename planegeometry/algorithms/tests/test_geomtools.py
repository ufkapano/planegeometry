#!/usr/bin/python

import unittest
import math
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.algorithms.geomtools import orientation
from planegeometry.algorithms.geomtools import angle3points
from planegeometry.algorithms.geomtools import find_two_furthest_points1
from planegeometry.algorithms.geomtools import find_two_furthest_points2
from planegeometry.algorithms.geomtools import iter_all_antipodal_pairs
from planegeometry.algorithms.geomtools import find_intersection_points
from planegeometry.algorithms.geomtools import find_two_closest_points


class TestOrientation(unittest.TestCase):

#     o
# o o
# o o
    def setUp(self):
        self.p00 = Point(0, 0)
        self.p01 = Point(0, 1)
        self.p10 = Point(1, 0)
        self.p11 = Point(1, 1)
        self.p22 = Point(2, 2)

    def test_orientation(self):
        self.assertEqual(orientation(self.p00, self.p11, self.p22), 0)
        self.assertEqual(orientation(self.p00, self.p10, self.p22), 1)
        self.assertEqual(orientation(self.p00, self.p10, self.p11), 1)
        self.assertEqual(orientation(self.p10, self.p11, self.p01), 1)
        self.assertEqual(orientation(self.p00, self.p01, self.p22), -1)
        self.assertEqual(orientation(self.p00, self.p01, self.p11), -1)
        self.assertEqual(orientation(self.p01, self.p11, self.p10), -1)

    def test_angle3points(self):
        self.assertEqual(angle3points(self.p10, self.p00, self.p01), 0.5*math.pi)
        self.assertEqual(angle3points(self.p11, self.p01, self.p00), 1.5*math.pi)
        self.assertEqual(angle3points(self.p22, self.p11, self.p01), 0.75*math.pi)
        self.assertEqual(angle3points(self.p10, self.p01, self.p11), 0.25*math.pi)

    def tearDown(self): pass


class TestFurthestPoints(unittest.TestCase):

    def setUp(self): pass
# o---o
# |  /
# o-o
    def test_set1(self):
        L = [Point(0, 0), Point(1, 0), Point(2, 1), Point(0, 1)]
        pair = Point(0, 0), Point(2, 1)
        result = find_two_furthest_points1(L)
        self.assertEqual(result, pair)
        result = find_two_furthest_points2(L)
        self.assertEqual(result, pair)

    def test_set2(self):
        s = 5
        L = [Point(i, j) for i in range(s) for j in range(s)]
        pair = Point(0, 0), Point(s-1, s-1)
        result = find_two_furthest_points1(L)
        self.assertEqual(result, pair)
        # Musze przygotowac otoczke wypukla.
        L = [Point(0, 0), Point(s-1, 0), Point(s-1, s-1), Point(0, s-1)]
        result = find_two_furthest_points2(L)
        self.assertEqual(result, pair)

    def tearDown(self): pass


class TestAntipodalPoints(unittest.TestCase):

    def setUp(self): pass
# o
# | \
# |   o
# |  /
# o-o
    def test_polygon1(self): # nie ma rownoleglych krawedzi
        L = [Point(0, 0), Point(1, 0), Point(2, 1), Point(0, 2)]
        expected = [(Point(0, 0), Point(2, 1)),
            (Point(0, 0), Point(0, 2)),
            (Point(1, 0), Point(0, 2)),
            (Point(2, 1), Point(0, 2))]
        result = list(iter_all_antipodal_pairs(L))
        self.assertEqual(result, expected)
# o---o
# |  /
# o-o
    def test_polygon2(self): # jedna para krawedzi rownoleglych
        L = [Point(0, 0), Point(1, 0), Point(2, 1), Point(0, 1)]
        expected = [(Point(0, 0), Point(2, 1)),
            (Point(0, 0), Point(0, 1)),
            (Point(1, 0), Point(2, 1)),
            (Point(1, 0), Point(0, 1)),
            (Point(2, 1), Point(0, 1))]
        result = list(iter_all_antipodal_pairs(L))
        self.assertEqual(result, expected)
# o
# |\
# | o
# | |
# o-o
    def test_polygon3(self): # jedna para krawedzi rownoleglych
        L = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 2)]
        expected = [(Point(0, 0), Point(1, 0)),
            (Point(0, 0), Point(1, 1)),
            (Point(0, 0), Point(0, 2)),
            (Point(1, 0), Point(0, 2)),
            (Point(1, 1), Point(0, 2))]
        result = list(iter_all_antipodal_pairs(L))
        self.assertEqual(result, expected)
# o---o
# |   |
# o---o
    def test_polygon4(self): # prostokat
        L = [Point(0, 0), Point(2, 0), Point(2, 1), Point(0, 1)]
        expected = [(Point(0, 0), Point(2, 0)),
            (Point(0, 0), Point(2, 1)),
            (Point(0, 0), Point(0, 1)),
            (Point(2, 0), Point(2, 1)),
            (Point(2, 0), Point(0, 1)),
            (Point(2, 1), Point(0, 1))]
        result = list(iter_all_antipodal_pairs(L))
        self.assertEqual(result, expected)

    def test_polygon5(self): # pieciokat
        L = [Point(1, 0), Point(3, 0), Point(4, 2), Point(2, 3), Point(0, 2)]
        expected = [(Point(1, 0), Point(4, 2)),
            (Point(1, 0), Point(2, 3)),
            (Point(3, 0), Point(2, 3)),
            (Point(3, 0), Point(0, 2)),
            (Point(4, 2), Point(0, 2))]
        result = list(iter_all_antipodal_pairs(L))
        self.assertEqual(result, expected)

    def test_polygon6(self): # szesciokat symetryczny
        L = [Point(2, 0), Point(4, 1), Point(4, 3), Point(2, 4),
            Point(0, 3), Point(0, 1)]
        expected = [(Point(2, 0), Point(4, 3)),
            (Point(2, 0), Point(2, 4)),
            (Point(2, 0), Point(0, 3)),
            (Point(4, 1), Point(2, 4)),
            (Point(4, 1), Point(0, 3)),
            (Point(4, 1), Point(0, 1)),
            (Point(4, 3), Point(0, 3)),
            (Point(4, 3), Point(0, 1)),
            (Point(2, 4), Point(0, 1))]
        result = list(iter_all_antipodal_pairs(L))
        self.assertEqual(result, expected)
#       o
#     //
#   o  /
#  /   /
# o   o
# |  /
# o-o
    def test_polygon7(self): # szesciokat
        L = [Point(0, 0), Point(1, 0), Point(2, 1), Point(3, 3),
            Point(1, 2), Point(0, 1)]
        expected = [(Point(0, 0), Point(3, 3)),
            (Point(1, 0), Point(3, 3)),
            (Point(1, 0), Point(1, 2)),
            (Point(1, 0), Point(0, 1)),
            (Point(2, 1), Point(1, 2)),
            (Point(2, 1), Point(0, 1)),
            (Point(3, 3), Point(0, 1))]
        result = list(iter_all_antipodal_pairs(L))
        self.assertEqual(result, expected)

    def test_polygon8(self): # trojkat
        L = [Point(0, 0), Point(2, 0), Point(1, 2)]
        expected = [(Point(0, 0), Point(2, 0)),
            (Point(0, 0), Point(1, 2)),
            (Point(2, 0), Point(1, 2))]
        result = list(iter_all_antipodal_pairs(L))
        self.assertEqual(result, expected)

    def tearDown(self): pass


class TestIntersectionPoints(unittest.TestCase):

    def setUp(self):
        self.segment_list = []
        self.segment_list.append(Segment(9, 11, 0, 2))
        self.segment_list.append(Segment(4, 0, 11, 7))
        self.segment_list.append(Segment(10, 2, 1, 11))
        self.segment_list.append(Segment(2, 6, 7, 1))

    def test_intersections(self):
        result = find_intersection_points(self.segment_list)
        result.sort()
        expected = [Point(3, 5), Point(5, 7), Point(6, 2), Point(8, 4)]
        self.assertEqual(result, expected)

    def tearDown(self): pass


class TestClosestPoints(unittest.TestCase):

    def setUp(self):
        self.point_list = [Point(2, 8), Point(0, 7), Point(5, 6),
            Point(4, 3), Point(7, 2), Point(6, 1), Point(3, 0)]
        self.result = (Point(6, 1), Point(7, 2))

        self.points1 = list()
        self.points1.append(Point(-19, -10))
        self.points1.append(Point(-16, 2))
        self.points1.append(Point(-12, -3))
        self.points1.append(Point(-10, 10))
        self.points1.append(Point(-9, 5))
        self.points1.append(Point(-5, -5))
        self.points1.append(Point(-4, -9))
        self.points1.append(Point(-3, 9))
        self.points1.append(Point(-2, 5))
        self.points1.append(Point(-1, 7))
        self.points1.append(Point(2, 4))
        self.points1.append(Point(6, 13))
        self.points1.append(Point(4, 15))
        self.points1.append(Point(11, -3))
        self.points1.append(Point(14, 3))
        self.points1.append(Point(27, 10))
        self.points1.append(Point(5, -9))
        self.points1.append(Point(8, -4))
        self.points1.append(Point(3, -4))
        self.points1.append(Point(15, -13))
        self.points1.append(Point(17, -7))
        self.points1.append(Point(25, 6))
        self.points1.append(Point(20, 3))
        self.points1.append(Point(24, -2))
        self.result1 = (Point(-2, 5), Point(-1, 7))

        self.points2 = list()
        self.points2.append(Point(1, 3))
        self.points2.append(Point(4, 3))
        self.result2 = (Point(1, 3), Point(4, 3))

        self.points3 = list()
        self.points3.append(Point(1, 3))
        self.points3.append(Point(4, 3))
        self.points3.append(Point(0, 0))
        self.result3 = (Point(1, 3), Point(4, 3))

    def test_closest_points(self):
        pair = find_two_closest_points(self.point_list)
        pair1 = find_two_closest_points(self.points1)
        pair2 = find_two_closest_points(self.points2)
        pair3 = find_two_closest_points(self.points3)
        self.assertEqual(sorted(pair), sorted(self.result))
        self.assertEqual(sorted(pair1), sorted(self.result1))
        self.assertEqual(sorted(pair2), sorted(self.result2))
        self.assertEqual(sorted(pair3), sorted(self.result3))

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()     # wlacza wszystkie testy

# EOF
