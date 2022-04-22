#!/usr/bin/env python3

import unittest
from planegeometry.structures.events import Event
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment


class TestEvents(unittest.TestCase):

    def setUp(self):
        segment1 = Segment(0, 0, 4, 4)
        segment2 = Segment(1, 3, 3, 1)
        self.event1 = Event(segment1.pt1, Event.LEFT, segment1)
        self.event2 = Event(segment1.pt2, Event.RIGHT, segment1)
        self.event3 = Event(Point(2, 2), Event.CROSSING, segment2, segment1)
        segment3 = Segment(0, 0, 0, 1)
        segment4 = Segment(0, 0, 1, 0)
        self.event4 = Event(segment3.pt1, Event.VERTICAL, segment3)
        self.event5 = Event(segment4.pt1, Event.HORIZONTAL, segment4)

    def test_cmp(self):
        self.assertTrue(self.event1 == self.event4)
        self.assertFalse(self.event1 == self.event2)
        self.assertTrue(self.event1 != self.event2)
        self.assertFalse(self.event1 != self.event4)
        self.assertTrue(self.event1 < self.event2)
        self.assertFalse(self.event3 < self.event1)
        self.assertTrue(self.event1 <= self.event2)
        self.assertFalse(self.event3 <= self.event1)
        self.assertTrue(self.event3 > self.event1)
        self.assertFalse(self.event1 > self.event2)
        self.assertTrue(self.event3 >= self.event1)
        self.assertFalse(self.event1 >= self.event3)

    def test_hash(self):
        aset = set()
        aset.add(self.event1)
        aset.add(self.event2)
        aset.add(self.event2)   # ignored
        self.assertEqual(len(aset), 2)
        aset.add(self.event3)
        aset.add(self.event3)
        self.assertEqual(len(aset), 3)

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
