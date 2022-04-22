#!/usr/bin/env python3

import unittest
from planegeometry.structures.avltree1 import AVLTree


class TestAVLTree(unittest.TestCase):

    def setUp(self): pass

    def test_avl(self):
        tree = AVLTree()
        self.assertTrue(tree.root is None)
        tree.insert(10)
        self.assertEqual(tree.root.value, 10)
        tree.insert(11)
        self.assertEqual(tree.root.right.value, 11)
        tree.insert(12)
        self.assertEqual(tree.root.value, 11)
        self.assertEqual(tree.root.left.value, 10)
        self.assertEqual(tree.root.right.value, 12)
        tree.insert(5)
        tree.insert(4)
        self.assertEqual(tree.root.left.value, 5)
        self.assertEqual(tree.root.left.left.value, 4)
        self.assertEqual(tree.root.left.right.value, 10)
        tree.insert(16)
        tree.insert(15)
        self.assertEqual(tree.root.right.value, 15)
        self.assertEqual(tree.root.right.left.value, 12)
        self.assertEqual(tree.root.right.right.value, 16)
        tree.remove(12)
        self.assertEqual(tree.root.right.left, None)
        tree.remove(15)
        self.assertEqual(tree.root.right.value, 16)
        tree.remove(5)
        self.assertEqual(tree.root.left.value, 10)
        tree.remove(11)   # root
        self.assertEqual(tree.root.value, 10)
        self.assertEqual(tree.root.left.value, 4)
        self.assertEqual(tree.root.right.value, 16)

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
