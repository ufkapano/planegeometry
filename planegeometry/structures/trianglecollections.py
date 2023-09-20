#!/usr/bin/env python3

from planegeometry.structures.points import Point
from planegeometry.structures.triangles import Triangle
from planegeometry.structures.graphs import Graph

class TriangleCollection:
    """The class defining a triangle collection."""

    def __init__(self):
        """Make a collection of triangles."""
        #self.items = []
        self.items = set()   # faster

    def __str__(self):
        """String representation of a triangle collection."""
        return str(self.items)

    def __len__(self):
        """Return the number of triangles in the collection."""
        return len(self.items)

    def itertriangles(self):
        """Generate triangles on demand."""
        return iter(self.items)

    def insert(self, triangle):
        """Insert a triangle to the collection."""
        if not isinstance(triangle, Triangle):
            raise ValueError("not a triangle")
        if triangle in self.items:   # O(1) time for sets
            raise ValueError("repeated triangle")
        #self.items.append(triangle)   # for lists
        self.items.add(triangle)   # for sets
        #print ( "tc.insert {}".format(triangle) )

    def remove(self, triangle):
        """Remove a triangle from the collection."""
        self.items.remove(triangle)   # O(1) time for sets
        #print ( "tc.remove {}".format(triangle) )

    def search(self, point):
        """Finding triangles containing a point."""
        result = []
        for triangle in self.items:   # O(n_t) time
            if point in triangle:
                result.append(triangle)
        return result

    def __contains__(self, other):
        """Test if a triangle is in a collection in O(1) time."""
        if isinstance(other, Triangle):
            return other in self.items   # O(1) time for sets
        else:
            raise ValueError("not a triangle")

    def to_graph(self):
        """Return the triangulation as a graph."""
        graph = Graph()
        for triangle in self.items:
            for segment in triangle.itersegments():
                if not graph.has_edge(segment):
                    graph.add_edge(segment)
        return graph

# EOF
