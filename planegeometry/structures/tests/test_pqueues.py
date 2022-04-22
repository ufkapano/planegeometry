#!/usr/bin/env python3

import unittest
from planegeometry.structures.pqueues import PriorityQueue

class TestPriorityQueue(unittest.TestCase):

    def setUp(self): pass

    def test_pq(self):
        pq = PriorityQueue()
        self.assertTrue(pq.empty())
        self.assertEqual(len(pq), 0)
        self.assertEqual(str(pq), "[]")
        pq.push(3)
        self.assertFalse(pq.empty())
        self.assertEqual(len(pq), 1)
        self.assertEqual(str(pq), "[3]")
        pq.push(3)   # ignored
        self.assertEqual(len(pq), 1)
        pq.push(5)
        self.assertEqual(len(pq), 2)
        pq.push(2)
        self.assertEqual(str(pq), "[2, 5, 3]")   # heap
        self.assertEqual(len(pq), 3)
        self.assertEqual(pq.pop(), 2)
        self.assertEqual(pq.pop(), 3)
        self.assertEqual(pq.pop(), 5)

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
