#!/usr/bin/env python3

import unittest
from planegeometry.structures.segments import Segment
from planegeometry.structures.slowtrees import SlowTree

class TestSlowTree(unittest.TestCase):

    def setUp(self):
        self.st = SlowTree()
        self.s1 = Segment(0, 0, 4, 4)
        self.s2 = Segment(1, 3, 3, 1)
        self.st.insert(self.s1)
        self.st.insert(self.s2)
        # Events:
        # Point(0,0) begin s1
        # Point(1,3) begin s2
        # Point(2,2) intersection
        # Point(3,1) end s2
        # Point(4,4) end s1

    def test_insert(self):
        self.assertEqual(len(self.st), 2)
        # Now s2 is above s1.
        #print ( self.st )
        self.assertEqual(self.st.successor(self.s1).value, self.s2)
        self.assertEqual(self.st.successor(self.s2), None)
        self.assertEqual(self.st.predecessor(self.s1), None)
        self.assertEqual(self.st.predecessor(self.s2).value, self.s1)
        # W punkcie przeciecia nastepuje zamiana odcinkow miejscami.
        self.st.swap(self.s1, self.s2)
        # Now s1 is above s2.
        #print ( self.st )
        self.assertEqual(self.st.successor(self.s2).value, self.s1)
        self.assertEqual(self.st.successor(self.s1), None)
        self.assertEqual(self.st.predecessor(self.s2), None)
        self.assertEqual(self.st.predecessor(self.s1).value, self.s2)

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
