#!/usr/bin/env python3

import math
import itertools
try:
    integer_types = (int, long)
    range = xrange
except NameError:   # Python 3
    integer_types = (int,)

# https://www.geeksforgeeks.org/orientation-3-ordered-points/
#
# Orientation of 3 ordered points.
# Values changed from (0, 2, 1) to (0, 1, -1).
# [2008 Kettner Mehlhorn Pion Schirra Yap] the same convention
#
# |pt1.x pt1.y 1|   returns the sign of the determinant
# |pt2.x pt2.y 1|
# |pt3.x pt3.y 1|

def orientation(pt1, pt2, pt3):
    """Orientation of 3 ordered points."""
    result = (pt2 - pt1).cross(pt3 - pt1)
    if result == 0:   # points are colinear
        return 0
    elif result > 0:   # left turn (counterclockwise)
        return 1
    else:   # right turn (clockwise)
        return -1

def oriented_area(pt1, pt2, pt3):
    # Funkcja moze zwracac int, float, Fraction, a wiec nie mozna
    # jej uzyc do porownywania przy sortowaniu (Graham).
    """Return the oriented area of a parallelogram."""
    return (pt2 - pt1).cross(pt3 - pt1)

def angle3points(a, b, c):
    """Counterclockwise angle in radians by turning from a to c around b
        Returns a float between 0.0 and 2*math.pi.
    
    https://python-forum.io/Thread-finding-angle-between-three-points-on-a-2d-graph
    """
    angle = math.atan2(c.y-b.y, c.x-b.x) - math.atan2(a.y-b.y, a.x-b.x)
    return angle + 2*math.pi if angle < 0 else angle

def find_two_furthest_points1(point_list):
    """Find two furthest points in O(n^2) time (brute force)."""
    dist2 = 0
    pair = None
    n = len(point_list)
    for i in range(n):
        for j in range(i+1, n):
            vec = point_list[j] - point_list[i]
            new_dist2 = vec * vec
            if new_dist2 > dist2:
                dist2 = new_dist2
                pair = point_list[i], point_list[j]
    return pair

def find_two_furthest_points3(point_list):
    """Find two furthest points in O(n^2) time (brute force)."""
    return max(itertools.combinations(point_list, 2),
        key=lambda pair: (pair[0]-pair[1])*(pair[0]-pair[1]))

def iter_all_antipodal_pairs(point_list):
    """Generate all antipodal pairs for a convex polygon (rotating calipers)."""
    # Orientacja punktow powinna byc anti-clockwise.
    # Wielokat nie moze miec sasiednich krawedzi wspolliniowych.
    # Preparata, Shamos, s.183
    L = point_list
    n = len(L)   # liczba punktow wielokata wypuklego
    i = n-1   # ostatni
    j = 0   # nastepny po i
    # Szukamy punktu polozonego najdalej od odcinka L[n-1]L[0].
    # Prosta wspierajaca zawiera ten odcinek.
    while (oriented_area(L[i], L[(i+1) % n], L[(j+1) % n]) >
        oriented_area(L[i], L[(i+1) % n], L[j])):
        j = (j + 1) % n
        #print ( "pierwsze while, j++ {}".format(j) )
    k = j   # najdalszy punkt
    # i zmienia sie od n-1 do k, j zmienia sie od k do n-1.
    #while j != 0: # to while zmienia i
    while True: # to while zmienia i
        i = (i + 1) % n   # przejscie na koniec odcinka i print
        #print ( "drugie while, i++ {}".format(i) )
        #print (i, j)
        yield L[i], L[j]   # raportuje pierwsza pare (0, k), potem nastepne
        # To while zmienia j, znowu szukamy najdalszego punktu.
        # Petla moze sie zatrzymac na krawedziach rownoleglych.
        while (oriented_area(L[i], L[(i+1) % n], L[(j+1) % n]) >
            oriented_area(L[i], L[(i+1) % n], L[j])):
            j = (j + 1) % n
            #print ( "trzecie while, j++ {}".format(j) )
            if j == 0: # nie mozna przekroczyc n-1
                return
            #if (i, j) != (k, 0):
            #    print (i, j)
            #    yield L[i], L[j]
            #else:
            #    return
            #print (i, j)
            yield L[i], L[j]
        # Obsluga krawedzi rownoleglych.
        if (oriented_area(L[i], L[(i+1) % n], L[(j+1) % n]) ==
            oriented_area(L[i], L[(i+1) % n], L[j])):
            #if (i, j) != (k, n-1): # czyli j < n-1 powinno byc
            if j != (n-1): # nie chcemy wypisac j=0
                # Bierzemy nastepne j, ale nie przesuwamy j.
                #print ( "{} {}".format((i, (j+1) % n), "rownolegle") )
                yield L[i], L[(j+1) % n]

def find_two_furthest_points2(point_list):
    """Find two furthest points in O(n) time for a convex polygon."""
    dist2 = 0
    pair = None
    for (pt1, pt2) in iter_all_antipodal_pairs(point_list):
        vec = pt2 - pt1
        new_dist2 = vec * vec
        if new_dist2 > dist2:
            dist2 = new_dist2
            pair = pt1, pt2
    return pair

def find_two_furthest_points4(point_list):
    """Find two furthest points in O(n) time for a convex polygon."""
    return max(iter_all_antipodal_pairs(point_list),
        key=lambda pair: (pair[0]-pair[1])*(pair[0]-pair[1]))

def find_intersection_points(segment_list):
    """Find intersection points for a segment list in O(n^2) time."""
    intersection_list = []
    n = len(segment_list)
    for i in range(n):
        for j in range(i+1, n):
            point = segment_list[i].intersection_point(segment_list[j])
            if point:
                intersection_list.append(point)
    return intersection_list

def find_two_closest_points(point_list):
    """Find two closest points in O(n^2) time (brute force)."""
    pair = point_list[0], point_list[1]
    vec = point_list[1] - point_list[0]
    dist2 = vec * vec
    n = len(point_list)
    for i in range(n):
        for j in range(i+1, n):
            vec = point_list[j] - point_list[i]
            new_dist2 = vec * vec
            if new_dist2 < dist2:
                dist2 = new_dist2
                pair = point_list[i], point_list[j]
    return pair

# EOF
