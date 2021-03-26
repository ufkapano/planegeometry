#!/usr/bin/python

import unittest
from fractions import Fraction
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.structures.polygons import Polygon
from planegeometry.structures.polygons import bounding_box
from planegeometry.structures.polygons import crossing_number
from planegeometry.structures.polygons import crossing_number2
from planegeometry.structures.polygons import winding_number

class TestPolygon(unittest.TestCase):

    def setUp(self):
        # kwadrat, orientacja +1
        self.polygon1 = Polygon(0, 0, 1, 0, 1, 1, 0, 1)
        # trojkat, orientacja +1
        self.polygon2 = Polygon(Point(0, 0), Point(2, 0), Point(1, 2))
        # o-o   nie jest wypukly, orientacja clockwise -1
        # | |
        # | o-o
        # |   |
        # o---o
        self.polygon3 = Polygon(0, 0, 0, 2, 1, 2, 1, 1, 2, 1, 2, 0)
        # o-o   nie jest prosty
        #  X
        # o-o
        self.polygon4 = Polygon(0, 0, 1, 0, 0, 1, 1, 1)

    def test_init(self):
        self.assertRaises(ValueError, Polygon, 0, 1, 2, 3)
        self.assertRaises(ValueError, Polygon, 0, 1, 2, 3, 4, 5, 6)
        self.assertRaises(ValueError, Polygon, Point(0, 1), Point(2, 3))
        self.assertRaises(ValueError, Polygon, Point(0, 1), Point(2, 3), Point(2, 3))
        self.assertRaises(ValueError, Polygon, 0, 0, 1, 0, 1, 1, 0, 0)

    def test_cmp(self):
        polygon3 = Polygon(0, 0, 2, 0, 1, 2)
        self.assertEqual(polygon3, self.polygon2)
        self.assertNotEqual(polygon3, self.polygon1)

    def test_print(self):
        self.assertEqual(repr(self.polygon1),
        "Polygon(Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1))")
        self.assertEqual(repr(self.polygon2),
        "Polygon(Point(0, 0), Point(2, 0), Point(1, 2))")

    def test_move(self):
        self.assertEqual(self.polygon1.move(2, 3), Polygon(2, 3, 3, 3, 3, 4, 2, 4))
        self.assertEqual(self.polygon2.move(Point(1, 2)), Polygon(1, 2, 3, 2, 2, 4))
        self.assertRaises(ValueError, Polygon.move, self.polygon1, 1)

    def test_copy(self):
        polygon3 = self.polygon2.copy()
        self.assertEqual(polygon3, self.polygon2)
        self.assertNotEqual(id(polygon3), id(self.polygon2))

    def test_orientation(self):
        self.assertEqual(self.polygon1.orientation(), 1)
        self.assertEqual(self.polygon2.orientation(), 1)
        self.assertEqual(self.polygon3.orientation(), -1)

    def test_is_simple(self):
        self.assertTrue(self.polygon1.is_simple())
        self.assertTrue(self.polygon3.is_simple())
        self.assertFalse(self.polygon4.is_simple())

    def test_is_convex(self):
        self.assertTrue(self.polygon1.is_convex())
        self.assertTrue(self.polygon2.is_convex())
        self.assertFalse(self.polygon3.is_convex())
        self.assertRaises(ValueError, self.polygon4.is_convex)

    def test_bounding_box(self):
        point_list = [Point(1, 0), Point(0, 1), Point(1, 2), Point(3, 1)]
        result = bounding_box(point_list)
        self.assertEqual(result, Polygon(0, 0, 3, 0, 3, 2, 0, 2))

    def test_contains(self):
        self.assertTrue(Point(Fraction(1, 2), Fraction(1, 2)) in self.polygon1)
        self.assertTrue(Point(0, 0) in self.polygon1)
        self.assertTrue(Point(-1, 0) not in self.polygon1)
        self.assertTrue(Point(-1, 1) not in self.polygon1)
        self.assertTrue(Point(1, 1) not in self.polygon1)
        self.assertTrue(Point(1, 1) in self.polygon2)
        self.assertTrue(Point(0, 2) not in self.polygon2)
        self.assertTrue(Point(-1, 0) not in self.polygon2)
        self.assertTrue(Point(1, 0) in self.polygon2)
        self.assertTrue(Point(Fraction(1, 2), 1) in self.polygon2)

    def test_iterpoints(self):
        self.polygon1 = Polygon(0, 0, 1, 0, 1, 1, 0, 1)
        L = list(self.polygon1.iterpoints())
        self.assertEqual(L[0], Point(0, 0))
        self.assertEqual(L[1], Point(1, 0))
        self.assertEqual(L[2], Point(1, 1))
        self.assertEqual(L[3], Point(0, 1))

    def test_itersegments(self):
        L = list(self.polygon3.itersegments())
        self.assertTrue(Segment(0, 0, 0, 2) in L)
        self.assertTrue(Segment(0, 2, 1, 2) in L)
        self.assertTrue(Segment(1, 1, 1, 2) in L)
        self.assertTrue(Segment(1, 1, 2, 1) in L)
        self.assertTrue(Segment(2, 0, 2, 1) in L)
        self.assertTrue(Segment(0, 0, 2, 0) in L)

    def test_hash(self):
        aset = set()
        aset.add(self.polygon1)
        aset.add(self.polygon1)   # ignored
        self.assertEqual(len(aset), 1)
        aset.add(self.polygon2)
        self.assertEqual(len(aset), 2)

    def tearDown(self): pass


class TestPointInPolygon(unittest.TestCase):

    def setUp(self): pass

# x o   x
#  /  \
# o x   o
#  \  /
# x o
    def test_simple_convex_polygon(self):
        point_list = [Point(1, 0), Point(3, 1), Point(1, 2), Point(0, 1)]
        polygon = Polygon(*point_list)
        # punkt w srodku
        point = Point(1, 1)
        self.assertEqual(crossing_number(polygon, point), 1)
        self.assertEqual(crossing_number2(polygon, point), 1)
        self.assertEqual(winding_number(polygon, point), 1)
        # punkt na zewnatrz
        point = Point(3, 2)
        self.assertEqual(crossing_number(polygon, point), 0)
        self.assertEqual(crossing_number2(polygon, point), 0)
        self.assertEqual(winding_number(polygon, point), 0)
        # punkt na zewnatrz, promien przecina wierzcholek gorny
        point = Point(0, 2)
        self.assertEqual(crossing_number(polygon, point), 0)
        self.assertEqual(crossing_number2(polygon, point), 0)
        self.assertEqual(winding_number(polygon, point), 0)
        # punkt na zewnatrz, promien przecina wierzcholek dolny ROZNICA
        point = Point(0, 0)
        self.assertEqual(crossing_number(polygon, point), 2)
        self.assertEqual(winding_number(polygon, point), 0)
        # punkt na lewej dolnej krawedzi (nalezy)
        point = Point(Fraction(1, 2), Fraction(1, 2))
        self.assertEqual(crossing_number(polygon, point), 1)
        self.assertEqual(crossing_number2(polygon, point), 1)
        self.assertEqual(winding_number(polygon, point), 1)
        # punkt na prawej gornej krawedzi (nie nalezy)
        point = Point(2, Fraction(3, 2))
        self.assertEqual(crossing_number(polygon, point), 0)
        self.assertEqual(crossing_number2(polygon, point), 0)
        self.assertEqual(winding_number(polygon, point), 0)

# x o   o
# x |\ /|
# x |xo |
#   |x  |
# x o---o
    def test_simple_concave_polygon(self):
        point_list = [Point(0, 0), Point(4, 0), Point(4, 4), Point(2, 2), Point(0, 4)]
        polygon = Polygon(*point_list)
        # punkt w srodku
        point = Point(1, 1)
        self.assertEqual(crossing_number(polygon, point), 1)
        self.assertEqual(crossing_number2(polygon, point), 1)
        self.assertEqual(winding_number(polygon, point), 1)
        # punkt na zewnatrz, promien w podstawie, ROZNICA
        point = Point(-1, 0)
        self.assertEqual(crossing_number(polygon, point), 2)
        self.assertEqual(crossing_number2(polygon, point), 2)
        self.assertEqual(winding_number(polygon, point), 0)
        # punkt na zewnatrz, promien w wierzcholkach
        point = Point(-1, 4)
        self.assertEqual(crossing_number(polygon, point), 0)
        self.assertEqual(crossing_number2(polygon, point), 0)
        self.assertEqual(winding_number(polygon, point), 0)
        # punkt na zewnatrz
        point = Point(-1, 3)
        self.assertEqual(crossing_number(polygon, point), 4)
        self.assertEqual(crossing_number2(polygon, point), 4)
        self.assertEqual(winding_number(polygon, point), 0)
        # punkt na zewnatrz, promien w wierzcholku 
        point = Point(-1, 2)
        self.assertEqual(crossing_number(polygon, point), 4)
        self.assertEqual(crossing_number2(polygon, point), 4)
        self.assertEqual(winding_number(polygon, point), 0)
        # punkt w srodku, promien w wierzcholku 
        point = Point(1, 2)
        self.assertEqual(crossing_number(polygon, point), 3)
        self.assertEqual(crossing_number2(polygon, point), 3)
        self.assertEqual(winding_number(polygon, point), 1)
        # punkt w srodku podstawy
        point = Point(2, 0)
        self.assertEqual(crossing_number(polygon, point), 1)
        self.assertEqual(crossing_number2(polygon, point), 1)
        self.assertEqual(winding_number(polygon, point), 1)
        # punkt w srodku boku \ (nie nalezy)
        point = Point(1, 3)
        self.assertEqual(crossing_number(polygon, point), 2)
        self.assertEqual(crossing_number2(polygon, point), 2)
        self.assertEqual(winding_number(polygon, point), 0)
        # punkt w srodku boku / (nalezy)
        point = Point(3, 3)
        self.assertEqual(crossing_number(polygon, point), 1)
        self.assertEqual(crossing_number2(polygon, point), 1)
        self.assertEqual(winding_number(polygon, point), 1)

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
