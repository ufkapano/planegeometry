#!/usr/bin/env python3

from typing import Any
from dataclasses import dataclass
from numbers import Real

@dataclass(frozen=True,repr=False)
class Edge:
    source: Any
    target: Any
    weight: Real = 1

    def __repr__(self):
        """Compute the string representation of the edge."""
        if self.weight == 1:
            return "Edge({0!r}, {1!r})".format(self.source, self.target)
        else:
            return "Edge({0!r}, {1!r}, {2!r})".format(
                self.source, self.target, self.weight)

    def __lt__(self, other):
        """Comparing of edges (the weight first)."""
        return (self.weight, self.source, self.target) < (
            other.weight, other.source, other.target)

    def __le__(self, other):
        """Comparing of edges (the weight first)."""
        return (self.weight, self.source, self.target) <= (
            other.weight, other.source, other.target)

    def __invert__(self):
        """Return the edge with the opposite direction."""
        return Edge(self.target, self.source, self.weight)

# EOF
