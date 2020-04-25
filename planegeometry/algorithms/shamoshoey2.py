#!/usr/bin/python

from planegeometry.structures.pqueues import PriorityQueue
from planegeometry.structures.events import Event
from planegeometry.structures.avltree2 import AVLTreeModified


class ShamosHoey:
    """Shamos-Hoey algorithm.
    
    http://geomalgorithms.com/a09-_intersect-3.html
    """

    def __init__(self, segment_list):
        self.eq = PriorityQueue()   # event queue (sorted along x)
        self.sl = AVLTreeModified()   # sweep line (sorted along y)

        for segment in segment_list:
            # Zalozone segment.pt1.x < segment.pt2.x.
            # Trzeba obsluzyc druga mozliwosc.
            if segment.pt1.x > segment.pt2.x:
                segment = ~segment
            self.eq.push(Event(segment.pt1, Event.LEFT, segment))
            self.eq.push(Event(segment.pt2, Event.RIGHT, segment))

    def run(self):
        while not self.eq.empty():
            event = self.eq.pop()
            if event.type == Event.LEFT:
                if self._handle_left_endpoint(event):
                    return True
            elif event.type == Event.RIGHT:
                if self._handle_right_endpoint(event):
                    return True
            else:
                raise ValueError("unknown event")
        return False

    def _handle_left_endpoint(self, event):
        segment_e = event.segment   # Let segE = E's segment

        self.sl.current_x = event.pt.x
        self.sl.insert(segment_e)   # Add segE to SL

        segment_above = self.sl.successor(segment_e)    # Let segA = the segment Above segE in SL
        segment_below = self.sl.predecessor(segment_e)  # Let segB = the segment Below segE in SL

        if segment_above:   # if exists
            segment_above = segment_above.value     # get segment from node
            if segment_e.intersect(segment_above):    # If (I = Intersect( segE with segA) exists)
                return True

        if segment_below:   # if exists
            segment_below = segment_below.value     # get segment from node
            if segment_e.intersect(segment_below):    # If (I = Intersect( segE with segB) exists)
                return True

        return False

    def _handle_right_endpoint(self, event):
        segment_e = event.segment  # Let segE = E's segment

        segment_above = self.sl.successor(segment_e)  # Let segA = the segment Above segE in SL
        segment_below = self.sl.predecessor(segment_e)  # Let segB = the segment Below segE in SL

        if segment_above and segment_below:     # if exists
            segment_above = segment_above.value     # get segment from node
            segment_below = segment_below.value     # get segment from node
            if segment_above.intersect(segment_below):    # If (I = Intersect( segA with segB) exists)
                return True

        self.sl.delete(segment_e)
        return False
