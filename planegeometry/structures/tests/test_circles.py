#!/usr/bin/env python3

import math
import unittest
from fractions import Fraction
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.structures.circles import Circle

class TestCircle(unittest.TestCase):

    def setUp(self):
        self.c1 = Circle(0, 0, 2)
        self.c2 = Circle(0, 0, 6)
        self.c3 = Circle(Point(1, 2), 3)
        self.c4 = Circle(Fraction(1, 3), Fraction(2, 3), Fraction(3, 4))

    def test_init(self):
        self.assertRaises(ValueError, Circle, 1, 2)
        self.assertRaises(ValueError, Circle, 1, Point(2, 2))
        self.assertRaises(ValueError, Circle, 0, 0, -1)
        self.assertRaises(ValueError, Circle, Point(0, 0), -1)
        self.assertEqual(self.c1.pt, Point(0, 0))
        self.assertEqual(self.c1.radius, 2)
        self.assertEqual(self.c3.pt, Point(1, 2))
        self.assertEqual(self.c3.radius, 3)

    def test_print(self):
        self.assertEqual(repr(self.c1), "Circle(0, 0, 2)")
        self.assertEqual(repr(self.c2), "Circle(0, 0, 6)")
        self.assertEqual(repr(self.c3), "Circle(1, 2, 3)")
        self.assertEqual(repr(self.c4), "Circle(Fraction(1, 3), Fraction(2, 3), Fraction(3, 4))")

    def test_copy(self):
        c3 = self.c1.copy()
        self.assertEqual(c3, self.c1)
        self.assertNotEqual(id(c3), id(self.c1))

    def test_center(self):
        self.assertEqual(self.c1.center(), Point(0, 0))
        self.assertEqual(self.c2.center(), Point(0, 0))
        self.assertEqual(self.c3.center(), Point(1, 2))
        self.assertEqual(self.c4.center(), Point(Fraction(1, 3), Fraction(2, 3)))

    def test_area(self):
        self.assertEqual(self.c1.area(), math.pi * 2 * 2)
        self.assertEqual(self.c2.area(), math.pi * 6 * 6)

    def test_move(self):
        self.assertEqual(self.c1.move(1, 2), Circle(1, 2, 2))
        self.assertEqual(self.c1.move(Point(1, 2)), Circle(1, 2, 2))
        self.assertEqual(self.c2.move(-1, -2), Circle(-1, -2, 6))
        self.assertRaises(ValueError, Circle.move, self.c1, 1)

    def test_cmp(self):
        self.assertTrue(self.c1 == Circle(0, 0, 2))
        self.assertFalse(self.c1 == self.c2)
        self.assertTrue(self.c1 != self.c2)
        self.assertFalse(self.c1 != Circle(0, 0, 2))
        self.assertTrue(self.c1 < self.c2)
        self.assertFalse(self.c3 < self.c2)
        self.assertTrue(self.c1 <= self.c3)
        self.assertFalse(self.c2 <= self.c1)
        self.assertTrue(self.c3 > self.c1)
        self.assertFalse(self.c2 > self.c3)
        self.assertTrue(self.c3 >= self.c1)
        self.assertFalse(self.c2 >= self.c3)

    def test_hash(self):
        aset = set()
        aset.add(self.c1)
        aset.add(self.c1)   # ignored
        self.assertEqual(len(aset), 1)
        aset.add(self.c2)
        self.assertEqual(len(aset), 2)
        aset.add(Circle(1, 2, 3))
        aset.add(Circle(1.0, 2.0, 3.0))   # ignored, float
        self.assertEqual(len(aset), 3)

    def test_cover(self):
        self.assertEqual(self.c1.cover(self.c2), self.c2) # c1 in c2
        #-2 -1  0  1  2  3  4
        # |--|--|--|--|--|--|
        # (.....o.....) c1
        #             (..o..)
        # (........o........) cover
        self.assertEqual(self.c1.cover(Circle(3, 0, 1)), Circle(1, 0, 3))

    def test_contains(self):
        self.assertTrue(Point(1, 1) in self.c1)
        self.assertFalse(Point(2, 2) in self.c1)
        self.assertTrue(Segment(0, 1, 1, 0) in self.c1)
        self.assertFalse(Segment(0, 0, 2, 2) in self.c1)
        self.assertTrue(Circle(0, 1, 1) in self.c1)
        self.assertTrue(Circle(0, 0, 2) in self.c1)
        self.assertFalse(Circle(0, 1, 2) in self.c1)
        self.assertRaises(ValueError, Circle.__contains__, self.c1, 1)

    def test_gnu(self):
        s1 = 'set label "" at 0.0,0.0 point pt 7 ps 0.5\n'
        s2 = 'set object circle at 0.0,0.0 size 2.0 fc rgb "black" fs empty\n'
        self.assertEqual(self.c1.gnu(True), s1 + s2)

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
