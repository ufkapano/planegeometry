# planegeometry package

Python implementation of algorithms and data structures
from plane geometry is presented.

## Problems, algorithms, and data structures

* Geometric objects: points, segments, polygons, rectangles, triangles, circles
* Data structures: edges, graphs, triangle collections, AVL trees, 
quadtrees, connected planar maps
* Point in polygon problem: the winding number method, the crossing number method
* Polygon orientation
* Bounding box
* Line segment intersection problem: 
brute force O(n^2), Shamos-Hoey, Bentley-Ottmann
* Closest pair of points problem: brute force search O(n^2), 
sweep line technique, divide and conquer approach
* Finding two furthest points: brute force search O(n^2), rotating calipers
* Convex hulls: Graham scan O(n log n), Jarvis march (gift wrapping) O(n h), 
quickhull (divide and conquer approach)
* Delaunay triangulations: naive approach O(n^4), edge flipping, Bowyer-Watson
* Convex polygons: recognition, fan triangulation O(n)
* Monotone polygons: recognition (in progress),
monotone triangulation, monotone partition
* Connected planar maps based on the doubly connected edge list (DCEL): 
constructors, map overlay procedure, mesh refinement (longest edge)
* Voronoi diagrams: from Delaunay triangulation
* Range searching: in progress

## Download

To install an official release do

    python3 -m pip install planegeometry

To get the git version do

    git clone https://github.com/ufkapano/planegeometry.git

## Usage

See doc/quickstart.txt and other doc/*.txt files.

## Contributors

Andrzej Kapanowski (project leader)

Marcin Permus (convex hull, rotating calipers)

Wojciech Chrobak (sweep line technique, quadtree, closest pair problem)

Monika Wiech (Delaunay triangulation)

Anna Sarnavska (planar maps overlay)

Gabriela Mazur (monotone polygons)

Mateusz Malczewski (Voronoi diagrams, polygon partition)

Maciej Mularski (range searching)

EOF
