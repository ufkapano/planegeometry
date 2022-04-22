#!/usr/bin/env python3

import unittest
import math
from fractions import Fraction
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment

class TestSegment(unittest.TestCase):

    def setUp(self):
        self.segment1 = Segment(0, 0, 2, 0)
        self.segment2 = Segment(Point(0, 0), Point(1, 1))
        self.segment3 = Segment(Fraction(1, 2), Fraction(2, 3),
            Fraction(3, 4), Fraction(4, 5))

    def test_init(self):
        self.assertRaises(ValueError, Segment, 0, 1)
        self.assertRaises(ValueError, Segment, 0, 1, 2)
        self.assertRaises(ValueError, Segment, Point(0, 1), 2)
        self.assertRaises(ValueError, Segment, 2, Point(0, 1))
        self.assertRaises(ValueError, Segment, 0, 1, 0, 1)
        self.assertRaises(ValueError, Segment, Point(0, 1), Point(0, 1))

    def test_print(self):
        self.assertEqual(repr(self.segment1), "Segment(0, 0, 2, 0)")
        self.assertEqual(repr(self.segment2), "Segment(0, 0, 1, 1)")
        self.assertEqual(repr(self.segment3),
        "Segment(Fraction(1, 2), Fraction(2, 3), Fraction(3, 4), Fraction(4, 5))")

    def test_cmp(self):
        self.assertEqual(Segment(), Segment(0, 0, 1, 1))
        self.assertTrue(self.segment1 == Segment(0, 0, 2, 0))
        self.assertFalse(self.segment1 == self.segment2)
        self.assertTrue(self.segment1 != self.segment2)
        self.assertFalse(self.segment1 != Segment(0, 0, 2, 0))
        self.assertTrue(self.segment2 < self.segment1)
        self.assertFalse(self.segment1 < self.segment2)
        self.assertTrue(self.segment2 <= self.segment1)
        self.assertFalse(self.segment1 <= self.segment2)
        self.assertTrue(self.segment3 > self.segment1)
        self.assertFalse(self.segment2 > self.segment3)
        self.assertTrue(self.segment3 >= self.segment1)
        self.assertFalse(self.segment2 >= self.segment1)

    def test_copy(self):
        segment3 = self.segment1.copy()
        self.assertEqual(segment3, self.segment1)
        self.assertNotEqual(id(segment3), id(self.segment1))

    def test_center(self):
        self.assertEqual(self.segment1.center(), Point(1, 0))
        self.assertEqual(self.segment2.center(), Point(0.5, 0.5))
        self.assertEqual(self.segment2.center(),
            Point(Fraction(1, 2), Fraction(1, 2)))

    def test_length(self):
        self.assertAlmostEqual(self.segment1.length(), 2)
        self.assertAlmostEqual(self.segment2.length(), math.sqrt(2))

    def test_move(self):
        self.assertEqual(self.segment1.move(1, 2), Segment(1, 2, 3, 2))
        self.assertEqual(self.segment1.move(Point(1, 2)), Segment(1, 2, 3, 2))
        self.assertRaises(ValueError, Segment.move, self.segment1, 1)

    def test_invert(self):
        self.assertEqual(~self.segment1, Segment(2, 0, 0, 0))
        self.assertEqual(~self.segment2, Segment(1, 1, 0, 0))

    def test_contains(self):
        self.assertTrue(Point(1, 0) in self.segment1)
        self.assertTrue(Point(1, 1) not in self.segment1)
        self.assertTrue(self.segment1.pt1 in self.segment1)
        self.assertTrue(self.segment1.pt2 in self.segment1)
        self.assertFalse(Point(6, 6) in self.segment1)
        self.assertFalse(Point(3, 0) in self.segment1)
        self.assertFalse(Point(-3, 0) in self.segment1)
        self.assertTrue(Point(0.5, 0.5) in self.segment2)
        self.assertTrue(Point(Fraction(1, 2), Fraction(1, 2)) in self.segment2)
        self.assertTrue(Point(Fraction(1, 3), Fraction(1, 3)) in self.segment2)
        self.assertRaises(ValueError, Segment.__contains__, self.segment1, 1)
        # segment1 in segment2
        self.assertTrue(Segment(0, 0, 1, 0) in self.segment1)
        self.assertFalse(self.segment2 in self.segment1)

    def test_intersect(self):
        self.assertTrue(self.segment1.intersect(self.segment2))
        self.assertTrue(self.segment1.intersect(Segment(1, -1, 1, 1))) # -|-
        self.assertTrue(self.segment1.intersect(Segment(1, 0, 3, 0))) # zachodza
        self.assertTrue(self.segment1.intersect(Segment(-1, 0, 3, 0))) # 1 w 2
        self.assertFalse(self.segment1.intersect(Segment(1, 1, 3, 3))) # / -
        self.assertFalse(self.segment1.intersect(Segment(3, -1, 3, 1))) # - |

    def test_intersection_point(self):
        s1 = Segment(0, 0, 3, 3)
        s2 = Segment(1, 3, 3, 1)
        s3 = Segment(1, 0, 1, 2)
        #print(s1.intersection_point(s2))
        self.assertEqual(s1.intersection_point(s2), Point(2, 2))
        self.assertEqual(self.segment1.intersection_point(s2), None)
        self.assertEqual(s1.intersection_point(s3), Point(1, 1))
        #print(s1.intersection_point(s3))
        self.assertEqual(s1.intersection_point(Segment(0, 1, 2, 1)), Point(1, 1))
        # Intersections at ends.
        self.assertEqual(self.segment1.intersection_point(self.segment2), Point(0, 0)) # L
        self.assertEqual(self.segment2.intersection_point(s3), Point(1, 1)) # T
        self.assertEqual(self.segment1.intersection_point(s3), Point(1, 0)) # T
        self.assertRaises(ValueError, Segment.intersection_point,
            self.segment2, s1)
        self.assertRaises(ValueError, Segment.intersection_point,
            self.segment1, Segment(1, 0, 3, 0))
        self.assertRaises(ValueError, Segment.intersection_point,
            s3, Segment(1, 1, 1, 3))

    def test_parallel(self):
        self.assertTrue(self.segment1.parallel(Segment(1, 1, 2, 1)))
        self.assertTrue(self.segment2.parallel(Segment(1, 0, 2, 1)))
        self.assertFalse(self.segment1.parallel(self.segment2))

    def test_perpendicular(self):
        self.assertTrue(self.segment1.perpendicular(Segment(1, 0, 1, 1)))
        self.assertTrue(self.segment2.perpendicular(Segment(1, 1, 2, 0)))
        self.assertFalse(self.segment1.perpendicular(self.segment2))

    def test_calculate(self):
        s1 = Segment(0, 0, 3, 3)
        self.assertEqual(s1.calculate_y(2), 2)
        self.assertEqual(s1.calculate_y(2.5), 2.5)
        self.assertEqual(s1.calculate_x(1), 1)
        self.assertEqual(s1.calculate_x(1.5), 1.5)

    def test_hash(self):
        aset = set()
        aset.add(self.segment1)
        aset.add(self.segment1)   # ignored
        self.assertEqual(len(aset), 1)
        aset.add(self.segment2)
        self.assertEqual(len(aset), 2)

    def test_gnu(self):
        s1 = 'set label "" at 0.0,0.0 point pt 7 ps 0.5\n'
        s2 = 'set label "" at 2.0,0.0 point pt 7 ps 0.5\n'
        s3 = 'set arrow from 0.0,0.0 to 2.0,0.0 nohead\n'
        self.assertEqual(self.segment1.gnu(True), s1 + s2 + s3)

    def test_property(self):
        self.assertEqual(self.segment1.source, Point(0, 0))
        self.assertEqual(self.segment1.target, Point(2, 0))
        self.assertEqual(self.segment2.source, Point(0, 0))
        self.assertEqual(self.segment2.target, Point(1, 1))
        self.assertEqual(self.segment1.weight, self.segment1.length())
        self.assertEqual(self.segment2.weight, self.segment2.length())

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
