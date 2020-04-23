#!/usr/bin/python

import unittest
from planegeometry.structures.segments import Segment
from planegeometry.algorithms.shamoshoey1 import ShamosHoey


class TestShamosHoey(unittest.TestCase):

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

        self.segments3 = []  # empty

        self.segments4 = []
        self.segments4.append(Segment(-9, 5, -4, -9))
        self.segments4.append(Segment(14, 3, 27, 10))

        self.segments5 = []
        self.segments5.append(Segment(-1, 1, 1, -1))
        self.segments5.append(Segment(-2, 0, 2, 0))
        self.segments5.append(Segment(-2, -2, 2, 2))

    def test_intersections(self):
        self.assertTrue(ShamosHoey(self.segments1).run())
        self.assertTrue(ShamosHoey(self.segments2).run())
        self.assertFalse(ShamosHoey(self.segments3).run())
        self.assertFalse(ShamosHoey(self.segments4).run())
        self.assertTrue(ShamosHoey(self.segments5).run())

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
