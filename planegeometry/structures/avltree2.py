#!/usr/bin/env python3
#
# https://rosettacode.org/wiki/AVL_tree#Python
# https://github.com/TylerSandman/py-bst
#
# value is a segment here.
# Events are sorted by x.
# AVLTree (sweep line) is sorting segments by y.

class Node:
    """The class defining a node."""

    def __init__(self, segment):
        self.value = segment
        self.parent = None
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.value)

    def calculate(self, x):
        return self.value.calculate_y(x)

    def insert(self, node, x):
        if node is None:
            return
        if node.calculate(x) < self.calculate(x):
            if self.left is None:
                node.parent = self
                self.left = node
            else:
                self.left.insert(node, x)
        else:
            if self.right is None:
                node.parent = self
                self.right = node
            else:
                self.right.insert(node, x)

    def find_min(self):
        current = self
        while current.left:
            current = current.left
        return current

    def find_max(self):
        current = self
        while current.right:
            current = current.right
        return current

    def successor(self):
        if self.right:
            return self.right.find_min()
        current = self
        while current.parent and current is current.parent.right:
            current = current.parent
        return current.parent

    def predecessor(self):
        if self.left:
            return self.left.find_max()
        current = self
        while current.parent and current is current.parent.left:
            current = current.parent
        return current.parent


def height(node):
    if node:
        return node.height
    else:
        return 0


def update_height(node):
    node.height = max(height(node.left), height(node.right)) + 1


class AVLTreeModified:
    """The class defining an AVL tree modified for the sweep line method."""

    def __init__(self):
        self.root = None
        self.D = dict()   # for (segment, node) pairs
        self.current_x = None

    def insert(self, value):
        node = Node(value)
        if self.root:
            self.root.insert(node, self.current_x)
        else:
            self.root = node
        self.D[value] = node
        self.rebalance(node)

    def find(self, value):
        return self.D.get(value)

    def delete(self, value):
        node = self.D.get(value)
        if node:
            if not (node.left or node.right):
                self._delete_leaf(node)
                del self.D[value]
            elif not (node.left and node.right):
                self._delete_leaf_parent(node)
                del self.D[value]
            else:
                self._delete_node(node)

    remove = delete

    def _delete_leaf(self, node):
        parent_node = node.parent
        if parent_node:
            if parent_node.left == node:
                parent_node.left = None
            else:
                parent_node.right = None
            self.rebalance(parent_node)
        else:
            self.root = None

    def _delete_leaf_parent(self, node):
        parent_node = node.parent
        if node.value == self.root.value:
            if node.right:
                self.root = node.right
                node.right = None
                self.root.parent = None
            else:
                self.root = node.left
                node.left = None
                self.root.parent = None
        else:
            if parent_node.right == node:
                if node.right:
                    parent_node.right = node.right
                    parent_node.right.parent = parent_node
                    node.right = None
                else:
                    parent_node.right = node.left
                    parent_node.right.parent = parent_node
                    node.left = None
            else:
                if node.right:
                    parent_node.left = node.right
                    parent_node.left.parent = parent_node
                    node.right = None
                else:
                    parent_node.left = node.left
                    parent_node.left.parent = parent_node
                    node.left = None
        self.rebalance(parent_node)

    def _switch_nodes(self, node1, node2):
        self.D[node1.value] = node2
        self.D[node2.value] = node1

        switch1 = node1
        switch2 = node2
        temp_value = switch1.value

        if switch1.value == self.root.value:
            self.root.value = node2.value
            switch2.value = temp_value
        elif switch2.value == self.root.value:
            switch1.value = self.root.value
            self.root.value = temp_value
        else:
            switch1.value = node2.value
            switch2.value = temp_value

    def _delete_node(self, node):
        if height(node.left) > height(node.right):
            to_switch = node.predecessor()
            self._switch_nodes(node, to_switch)

            if not (to_switch.right or to_switch.left):
                to_delete = node.predecessor()
                self._delete_leaf(to_delete)
            else:
                to_delete = node.predecessor()
                self._delete_leaf_parent(to_delete)
        else:
            to_switch = node.successor()
            self._switch_nodes(node, to_switch)

            if not (to_switch.right or to_switch.left):
                to_delete = node.successor()
                self._delete_leaf(to_delete)
            else:
                to_delete = node.successor()
                self._delete_leaf_parent(to_delete)

    def swap(self, value1, value2):
        self.delete(value1)
        self.delete(value2)
        self.insert(value1)
        self.insert(value2)

    def successor(self, value):
        node = self.D.get(value)
        return node and node.successor()

    def predecessor(self, value):
        node = self.D.get(value)
        return node and node.predecessor()

    def rebalance(self, node):
        while node:
            update_height(node)
            if height(node.left) >= 2 + height(node.right):
                if height(node.left.left) >= height(node.left.right):
                    self.right_rotate(node)
                else:
                    self.left_rotate(node.left)
                    self.right_rotate(node)
            elif height(node.right) >= 2 + height(node.left):
                if height(node.right.right) >= height(node.right.left):
                    self.left_rotate(node)
                else:
                    self.right_rotate(node.right)
                    self.left_rotate(node)
            node = node.parent

    def left_rotate(self, x):
        y = x.right
        y.parent = x.parent
        if y.parent is None:
            self.root = y
        else:
            if y.parent.left is x:
                y.parent.left = y
            elif y.parent.right is x:
                y.parent.right = y
        x.right = y.left
        if x.right:
            x.right.parent = x
        y.left = x
        x.parent = y
        update_height(x)
        update_height(y)

    def right_rotate(self, x):
        y = x.left
        y.parent = x.parent
        if y.parent is None:
            self.root = y
        else:
            if y.parent.left is x:
                y.parent.left = y
            elif y.parent.right is x:
                y.parent.right = y
        x.left = y.right
        if x.left:
            x.left.parent = x
        y.right = x
        x.parent = y
        update_height(x)
        update_height(y)
