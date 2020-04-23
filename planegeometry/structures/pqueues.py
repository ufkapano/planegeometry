#!/usr/bin/python

import heapq

class PriorityQueue:
    """A priority queue without repetitions with O(log n) time operations."""

    def __init__(self):
        self.heap = []
        self.item_set = set()   # quick search

    def __str__(self):
        return str(self.heap)

    def push(self, item):
        if item not in self.item_set:
            heapq.heappush(self.heap, item)
            self.item_set.add(item)

    put = push

    def pop(self):
        if not self.empty():
            item = heapq.heappop(self.heap)
            self.item_set.remove(item)
            return item
        else:
            raise ValueError("priority queue is empty")

    get = pop

    def empty(self):
        return len(self.heap) == 0

    def __len__(self):
        return len(self.heap)

# EOF
