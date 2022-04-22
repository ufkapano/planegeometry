#!/usr/bin/env python3

import unittest
from fractions import Fraction
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.algorithms.bentleyottmann2 import BentleyOttmann


class TestBentleyOttmann(unittest.TestCase):

    def setUp(self):
        self.segments1 = []

        self.segments1.append(Segment(3, -4, 15, -13))
        self.segments1.append(Segment(17, -7, 25, 6))
        self.segments1.append(Segment(20, 3, 24, -2))
        self.segments1.append(Segment(5, -9, 8, -4))
        self.segments1.append(Segment(14, 3, 27, 10))
        self.segments1.append(Segment(-16, 2, -12, -3))
        self.segments1.append(Segment(-9, 5, -4, -9))
        self.segments1.append(Segment(-19, -10, -10, 10))
        self.segments1.append(Segment(-5, 5, -1, 7))
        self.segments1.append(Segment(4, 15, 11, -3))
        self.segments1.append(Segment(-3, 9, -2, 5))
        self.segments1.append(Segment(2, 4, 6, 13))

        self.segments2 = []
        self.segments2.append(Segment(9, 11, 0, 2))
        self.segments2.append(Segment(4, 0, 11, 7))
        self.segments2.append(Segment(10, 2, 1, 11))
        self.segments2.append(Segment(2, 6, 7, 1))

        self.segments3 = []
        self.segments3.append(Segment(-10, 2, -2, 5))
        self.segments3.append(Segment(2, -2, 13, 4))

        self.segments4 = []
        self.segments4.append(Segment(-10, 10, 20, 3))
        self.segments4.append(Segment(-9, 4, -2, 3))
        self.segments4.append(Segment(-3, 2, 17, 7))
        self.segments4.append(Segment(3, 5, 6, 2))
        self.segments4.append(Segment(-6, 6, 7, 13))
        self.segments4.append(Segment(-15, 7, 5, 8))

    def test_run(self):
        points1 = [Point(Fraction(-1808, 125), Fraction(2, 25)),
                   Point(Fraction(-7, 3), Fraction(19, 3)),
                   Point(Fraction(722, 135), Fraction(173, 15)),
                   Point(Fraction(187, 29), Fraction(-191, 29)),
                   Point(Fraction(501, 23), Fraction(71, 92))]
        self.assertEqual(BentleyOttmann(self.segments1).run(), points1)

        points2 = [Point(3, 5), Point(5, 7), Point(6, 2), Point(8, 4)]
        self.assertEqual(BentleyOttmann(self.segments2).run(), points2)

        self.assertEqual(BentleyOttmann(self.segments3).run(), [])

        points4 = [Point(Fraction(-385, 127), Fraction(965, 127)),
                   Point(Fraction(-610, 301), Fraction(350, 43)),
                   Point(Fraction(-5, 17), Fraction(263, 34)),
                   Point(Fraction(21, 5), Fraction(19, 5)),
                   Point(Fraction(295, 29), Fraction(307, 58))]
        self.assertEqual(BentleyOttmann(self.segments4).run(), points4)

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
