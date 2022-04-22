#!/usr/bin/env python3

import unittest
from planegeometry.structures.segments import Segment
from planegeometry.algorithms.shamoshoey2 import ShamosHoey


class TestShamosHoey(unittest.TestCase):

    def setUp(self):
        self.segments1 = set()
        self.segments1.add(Segment(3, -4, 15, -13))
        self.segments1.add(Segment(17, -7, 25, 6))
        self.segments1.add(Segment(20, 3, 24, -2))
        self.segments1.add(Segment(5, -9, 8, -4))
        self.segments1.add(Segment(14, 3, 27, 10))
        self.segments1.add(Segment(-16, 2, -12, -3))
        self.segments1.add(Segment(-9, 5, -4, -9))
        self.segments1.add(Segment(-19, -10, -10, 10))
        self.segments1.add(Segment(-5, 5, -1, 7))
        self.segments1.add(Segment(4, 15, 11, -3))
        self.segments1.add(Segment(-3, 9, -2, 5))
        self.segments1.add(Segment(2, 4, 6, 13))

        self.segments2 = set()
        self.segments2.add(Segment(9, 11, 0, 2))
        self.segments2.add(Segment(4, 0, 11, 7))
        self.segments2.add(Segment(10, 2, 1, 11))
        self.segments2.add(Segment(2, 6, 7, 1))

        self.segments3 = set()  # empty

        self.segments4 = set()
        self.segments4.add(Segment(-9, 5, -4, -9))
        self.segments4.add(Segment(14, 3, 27, 10))

        self.segments5 = set()
        self.segments5.add(Segment(-1, 1, 1, -1))
        self.segments5.add(Segment(-2, 0, 2, 0))
        self.segments5.add(Segment(-2, -2, 2, 2))


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
