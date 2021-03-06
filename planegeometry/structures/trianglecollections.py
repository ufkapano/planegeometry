#!/usr/bin/python

from planegeometry.structures.points import Point
from planegeometry.structures.triangles import Triangle
from planegeometry.structures.graphs import Graph

class TriangleCollection:
    """The class defining a triangle collection."""

    def __init__(self):
        """Make a collection of triangles."""
        self.items = []

    def __str__(self):
        """String representation of a triangle collection."""
        return str(self.items)

    def __len__(self):
        """Return the number of triangles in the collection."""
        return len(self.items)

    def itertriangles(self):
        """Generate triangles on demand."""
        for triangle in self.items:
            yield triangle

    def insert(self, triangle):
        """Insert a triangle to the collection."""
        if not isinstance(triangle, Triangle):
            raise ValueError("not a triangle")
        self.items.append(triangle)
        #print ( "tc.insert {}".format(triangle) )

    def remove(self, triangle):
        """Remove a triangle from the collection."""
        self.items.remove(triangle)
        #print ( "tc.remove {}".format(triangle) )

    def search(self, point):
        """Finding triangles containing a point."""
        result = []
        for triangle in self.items:
            if point in triangle:
                result.append(triangle)
        return result

    def __contains__(self, other):
        """Test if a triangle is in a collection."""
        if isinstance(other, Triangle):
            return other in self.items
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
