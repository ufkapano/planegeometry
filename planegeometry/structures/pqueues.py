#!/usr/bin/python

import heapq

class PriorityQueue:
    """A priority queue without repetitions with O(log n) time operations."""

    def __init__(self):
        """Create an empty queue."""
        self.heap = []
        self.item_set = set()   # quick search

    def __str__(self):
        """Return string representation of the queue."""
        return str(self.heap)

    def push(self, item):
        """Put an item into the queue."""
        if item not in self.item_set:
            heapq.heappush(self.heap, item)
            self.item_set.add(item)

    put = push

    def pop(self):
        """Remove and return an item from the queue."""
        if not self.empty():
            item = heapq.heappop(self.heap)
            self.item_set.remove(item)
            return item
        else:
            raise ValueError("priority queue is empty")

    get = pop

    def empty(self):
        """Test if the queue is empty."""
        return len(self.heap) == 0

    def __len__(self):
        """Return the size of the queue."""
        return len(self.heap)

# EOF
