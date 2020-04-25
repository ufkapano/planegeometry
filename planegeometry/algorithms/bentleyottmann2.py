#!/usr/bin/python

from planegeometry.structures.pqueues import PriorityQueue
from planegeometry.structures.avltree2 import AVLTreeModified
from planegeometry.structures.events import Event

# No two line segment endpoints or crossings have the same x-coordinate
# No line segment endpoint lies upon another line segment
# No three line segments intersect at a single point.

# http://www.mif.pg.gda.pl/homepages/jmaksymiuk/WdGKiGO/WdGKiGO_part2.pdf
# https://en.wikipedia.org/wiki/Bentley%E2%80%93Ottmann_algorithm
# http://geomalgorithms.com/a09-_intersect-3.html
# http://page.mi.fu-berlin.de/panos/cg13/l03.pdf
# http://www.bowdoin.edu/~ltoma/teaching/cs3250-CompGeom/spring16/Lectures/cg-segmintersect.pdf

class BentleyOttmann:
    """Bentley-Ottmann algorithm."""

    def __init__(self, segment_list):
        self.eq = PriorityQueue()  # event queue
        self.sl = AVLTreeModified()  # sweep line

        for segment in segment_list:
            # Zalozone segment.pt1.x < segment.pt2.x.
            # Trzeba obsluzyc druga mozliwosc.
            if segment.pt1.x > segment.pt2.x:
                segment = ~segment
            self.eq.push(Event(segment.pt1, Event.LEFT, segment))
            self.eq.push(Event(segment.pt2, Event.RIGHT, segment))

        self.il = []  # intersection list

    def run(self):
        while not self.eq.empty():
            event = self.eq.pop()
            if event.type == Event.LEFT:
                self._handle_left_endpoint(event)
            elif event.type == Event.RIGHT:
                self._handle_right_endpoint(event)
            elif event.type == Event.CROSSING:
                self._handle_crossing(event)
            else:
                raise ValueError("unknown event")
        del self.eq
        del self.sl
        return self.il

    def _handle_left_endpoint(self, event):
        segment_e = event.segment  # Let segE = E's segment
        self.sl.current_x = event.pt.x
        self.sl.insert(segment_e)  # Add segE to SL

        segment_above = self.sl.successor(segment_e)  # Let segA = the segment Above segE in SL
        segment_below = self.sl.predecessor(segment_e)  # Let segB = the segment Below segE in SL

        if segment_above:  # if exists
            segment_above = segment_above.value  # get segment from node
            point = segment_e.intersection_point(segment_above)
            if point and point.x > event.pt.x:
                self.eq.push(Event(point, Event.CROSSING, segment_above, segment_e))

        if segment_below:  # if exists
            segment_below = segment_below.value  # get segment from node
            point = segment_e.intersection_point(segment_below)
            if point and point.x > event.pt.x:
                self.eq.push(Event(point, Event.CROSSING, segment_e, segment_below))

    def _handle_right_endpoint(self, event):
        segment_e = event.segment  # Let segE = E's segment

        self.sl.current_x = event.pt.x
        segment_above = self.sl.successor(segment_e)  # Let segA = the segment Above segE in SL
        segment_below = self.sl.predecessor(segment_e)  # Let segB = the segment Below segE in SL

        if segment_above and segment_below:  # if exists
            segment_above = segment_above.value  # get segment from node
            segment_below = segment_below.value  # get segment from node
            point = segment_above.intersection_point(segment_below)
            if point and point.x > event.pt.x:
                self.eq.push(Event(point, Event.CROSSING, segment_above, segment_below))

        self.sl.delete(segment_e)

    def _handle_crossing(self, event):
        self.il.append(event.pt)  # Add Es intersect point to the output list IL

        self.sl.current_x = event.pt.x
        # Let segE1 above segE2 be E's intersecting segments in SL
        segment_e1 = event.segment_above
        segment_e2 = event.segment_below

        # Swap their positions so that segE2 is now above segE1;
        self.sl.swap(segment_e1, segment_e2)

        segment_above_e2 = self.sl.successor(segment_e2)  # Let segA = the segment above segE2 in SL
        segment_below_e1 = self.sl.predecessor(segment_e1)  # Let segB = the segment below segE1 in SL

        if segment_above_e2:
            segment_above_e2 = segment_above_e2.value
            point = segment_above_e2.intersection_point(segment_e2)
            if point and point.x > event.pt.x:
                self.eq.push(Event(point, Event.CROSSING, segment_above_e2, segment_e2))

        if segment_below_e1:
            segment_below_e1 = segment_below_e1.value
            point = segment_below_e1.intersection_point(segment_e1)
            if point and point.x > event.pt.x:
                self.eq.push(Event(point, Event.CROSSING, segment_e1, segment_below_e1))
