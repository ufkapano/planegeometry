# planegeometry package

Python implementation of algorithms and data structures
from plane geometry is presented.
The planegeometry package is written with Python 2.7 and Python 3.2.

## Problems, algorithms, and data structures

* Geometric objects: points, segments, polygons, rectangles, triangles, circles
* Data structures: edges, graphs, triangle collections, AVL trees, 
quadtrees, connected maps
* Point in polygon problem: the winding number, the crossing number
* Polygon orientation
* Bounding box
* Line segment intersection problem: Shamos-Hoey, Bentley-Ottmann
* Closest pair of points problem: brute force search O(n^2), 
sweep line technique, divide and conquer approach
* Finding two furthest points: brute force search O(n^2), rotating calipers
* Convex hulls: Graham scan, Jarvis march (gift wrapping), 
quickhull (divide and conquer approach)
* Delaunay triangulations: naive approach O(n^4), edge flipping, Bowyer-Watson
* Monotone polygons: in progress
* Connected planar maps: in progress (map overlay)

## Installation

See doc/quickstart.txt

## Contributors

Andrzej Kapanowski (project leader)

Marcin Permus (convex hull, rotating calipers)

Wojciech Chrobak (sweep line technique, quadtree, closest pair problem)

Monika Wiech (Delaunay triangulation)

Gabriela Mazur (monotone polygons)

EOF
