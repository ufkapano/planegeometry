#!/usr/bin/env python3

import unittest
from fractions import Fraction
from planegeometry.structures.points2 import Point
from planegeometry.structures.segments2 import Segment
from planegeometry.structures.rectangles2 import Rectangle
from planegeometry.structures.rectangles2 import bounding_box
from planegeometry.structures.circles import Circle

class TestRectangle(unittest.TestCase):

    def setUp(self):
        self.r1 = Rectangle(Point(0, 0), Point(5, 6))
        self.r2 = Rectangle(Point(3, 4), Point(7, 8))
        self.r3 = Rectangle(Point(6, 7), Point(8, 8))
        self.r4 = Rectangle(Point(1, 2), Point(3, 4))
        self.r5 = Rectangle(Point(Fraction(1, 2), Fraction(2, 3)),
            Point(Fraction(3, 4), Fraction(4, 5)))

    def test_init(self):
        self.assertRaises(TypeError, Rectangle, 0, 4, -1, 6)
        self.assertRaises(TypeError, Rectangle, 0, 4, 2, 2)
        self.assertRaises(TypeError, Rectangle, 0, 0, 2)
        self.assertRaises(ValueError, Rectangle, 1, 2)
        self.assertRaises(ValueError, Rectangle, Point(1, 1), 2)
        self.assertRaises(ValueError, Rectangle, 1, Point(2, 2))
        self.assertEqual(self.r1.pt1, Point(0, 0))
        self.assertEqual(self.r1.pt2, Point(5, 6))
        self.assertEqual(self.r4.pt1, Point(1, 2))
        self.assertEqual(self.r4.pt2, Point(3, 4))

    def test_print(self):
        self.assertEqual(repr(self.r1), "Rectangle(Point(0, 0), Point(5, 6))")
        self.assertEqual(repr(self.r2), "Rectangle(Point(3, 4), Point(7, 8))")
        self.assertEqual(repr(self.r3), "Rectangle(Point(6, 7), Point(8, 8))")
        self.assertEqual(repr(self.r4), "Rectangle(Point(1, 2), Point(3, 4))")
        self.assertEqual(repr(self.r5),
        "Rectangle(Point(Fraction(1, 2), Fraction(2, 3)), Point(Fraction(3, 4), Fraction(4, 5)))")

    def test_cmp(self):
        self.assertTrue(self.r1 == Rectangle(Point(0, 0), Point(5, 6)))
        self.assertFalse(self.r1 == self.r2)
        self.assertTrue(self.r1 != self.r2)
        self.assertFalse(self.r1 != Rectangle(Point(0, 0), Point(5, 6)))
        self.assertTrue(self.r1 < self.r2)
        self.assertFalse(self.r3 < self.r2)
        self.assertTrue(self.r1 <= self.r2)
        self.assertFalse(self.r3 <= self.r2)
        self.assertTrue(self.r3 > self.r1)
        self.assertFalse(self.r2 > self.r3)
        self.assertTrue(self.r3 >= self.r1)
        self.assertFalse(self.r2 >= self.r3)

    def test_copy(self):
        r4 = self.r1.copy()
        self.assertEqual(r4, self.r1)

    def test_center(self):
        self.assertEqual(self.r1.center(), Point(2.5, 3))
        self.assertEqual(self.r2.center(), Point(5, 6))

    def test_area(self):
        self.assertEqual(self.r1.area(), 30)
        self.assertEqual(self.r2.area(), 16)

    def test_move(self):
        self.assertEqual(self.r1.move(1, 2), Rectangle(Point(1, 2), Point(6, 8)))
        self.assertEqual(self.r1.move(Point(1, 2)), Rectangle(Point(1, 2), Point(6, 8)))
        self.assertRaises(ValueError, Rectangle.move, self.r1, 1)

    def test_intersection(self):
        r5 = self.r1.intersection(self.r2)
        self.assertEqual(r5, Rectangle(Point(3, 4), Point(5, 6)))
        self.assertRaises(ValueError, Rectangle.intersection, self.r1, self.r3)

    def test_cover(self):
        r6 = self.r1.cover(self.r2)
        self.assertEqual(r6, Rectangle(Point(0, 0), Point(7, 8)))

    def test_make4(self):
        r1 = Rectangle(Point(0, 0), Point(2.5, 3))
        r2 = Rectangle(Point(2.5, 3), Point(5, 6))
        r3 = Rectangle(Point(0, 3), Point(2.5, 6))
        r4 = Rectangle(Point(2.5, 0), Point(5, 3))
        result = self.r1.make4()
        self.assertTrue(r1 in result)
        self.assertTrue(r2 in result)
        self.assertTrue(r3 in result)
        self.assertTrue(r4 in result)

    def test_make4_frac(self):
        r1 = Rectangle(Point(0, 0), Point(Fraction(5, 2), 3))
        r2 = Rectangle(Point(Fraction(5, 2), 3), Point(5, 6))
        r3 = Rectangle(Point(0, 3), Point(Fraction(5, 2), 6))
        r4 = Rectangle(Point(Fraction(5, 2), 0), Point(5, 3))
        result = self.r1.make4()
        self.assertTrue(r1 in result)
        self.assertTrue(r2 in result)
        self.assertTrue(r3 in result)
        self.assertTrue(r4 in result)

    def test_hash(self):
        aset = set()
        aset.add(self.r1)
        aset.add(self.r1)   # ignored
        aset.add(Rectangle(Point(0.0, 0.0), Point(5.0, 6.0)))   # ignored, float
        self.assertEqual(len(aset), 1)
        aset.add(self.r2)
        self.assertEqual(len(aset), 2)

    def test_contains(self):
        self.assertTrue(Point(1, 1) in self.r1)
        self.assertFalse(Point(1, 7) in self.r1)
        self.assertFalse(Point(7, 1) in self.r1)
        self.assertRaises(ValueError, Rectangle.__contains__, self.r1, 1)
        # segment in rectangle
        self.assertTrue(Segment(Point(1, 1), Point(2, 2)) in self.r1)
        self.assertFalse(Segment(Point(1, 1), Point(7, 7)) in self.r1)
        # circle in rectangle
        self.assertTrue(Circle(2, 2, 2) in self.r1)
        self.assertFalse(Circle(0, 0, 2) in self.r1)

    def test_is_square(self):
        self.assertTrue(self.r2.is_square())
        self.assertFalse(self.r1.is_square())

    def test_iterpoints(self):
        L = list(self.r1.iterpoints())
        self.assertEqual(L[0], Point(0, 0))
        self.assertEqual(L[1], Point(5, 0))
        self.assertEqual(L[2], Point(5, 6))
        self.assertEqual(L[3], Point(0, 6))

    def test_itersegments(self):
        r1 = Rectangle(Point(0, 0), Point(5, 6))
        L = list(r1.itersegments())
        self.assertTrue(Segment(Point(0, 0), Point(5, 0)) in L)
        self.assertTrue(Segment(Point(0, 0), Point(0, 6)) in L)
        self.assertTrue(Segment(Point(0, 6), Point(5, 6)) in L)
        self.assertTrue(Segment(Point(5, 0), Point(5, 6)) in L)

    def test_itersegments_oriented(self):
        r1 = Rectangle(Point(0, 0), Point(5, 6))
        L = list(r1.itersegments_oriented())
        self.assertTrue(Segment(Point(0, 0), Point(0, 6)) in L)
        self.assertTrue(Segment(Point(0, 6), Point(5, 6)) in L)
        self.assertTrue(Segment(Point(5, 6), Point(5, 0)) in L)
        self.assertTrue(Segment(Point(5, 0), Point(0, 0)) in L)

    def test_gnu(self):
        s1 = 'set label "" at 0.0,0.0 point pt 7 ps 0.5\n'
        s2 = 'set label "" at 5.0,6.0 point pt 7 ps 0.5\n'
        s3 = 'set label "" at 0.0,6.0 point pt 7 ps 0.5\n'
        s4 = 'set label "" at 5.0,0.0 point pt 7 ps 0.5\n'
        s5 = 'set object rectangle from 0.0,0.0 to 5.0,6.0 fs empty\n'
        self.assertEqual(self.r1.gnu(True), s1 + s2 + s3 + s4 + s5)

    def test_bounding_box(self):
        point_list = [Point(1, 0), Point(0, 1), Point(1, 2), Point(3, 1)]
        result = bounding_box(point_list)
        self.assertEqual(result, Rectangle(Point(0, 0), Point(3, 2)))

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
