#!/usr/bin/env python3
#
# Edges are comared as tuples (source, target, weight).

from typing import Any
from dataclasses import dataclass
from numbers import Real

@dataclass(frozen=True,order=True)
class Edge:
    source: Any
    target: Any
    weight: Real = 1

    def __invert__(self):
        """Return the edge with the opposite direction."""
        return Edge(self.target, self.source, self.weight)

# EOF
