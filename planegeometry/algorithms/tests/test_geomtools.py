#!/usr/bin/python

import unittest
from planegeometry.structures.points import Point
from planegeometry.algorithms.geomtools import orientation
from planegeometry.algorithms.geomtools import find_two_furthest_points1
from planegeometry.algorithms.geomtools import find_two_furthest_points2
from planegeometry.algorithms.geomtools import iter_all_antipodal_pairs


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

if __name__ == "__main__":

    unittest.main()     # wlacza wszystkie testy

# EOF
