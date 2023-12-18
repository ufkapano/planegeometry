#!/usr/bin/env python3

from planegeometry.structures.pqueues import PriorityQueue
from planegeometry.structures.events import Event
from planegeometry.structures.slowtrees import SlowTreeY


class ShamosHoey:
    """Shamos-Hoey algorithm - educational version.
    
    http://geomalgorithms.com/a09-_intersect-3.html
    """

    def __init__(self, segment_list):
        self.event_queue = PriorityQueue()   # sorted along x
        self.sweep_line = SlowTreeY()        # sorted along y

        for segment in segment_list:
            # Zalozone segment.pt1.x < segment.pt2.x.
            # Trzeba obsluzyc druga mozliwosc.
            if segment.pt1.x > segment.pt2.x:
                segment = ~segment
            self.event_queue.push(Event(segment.pt1, Event.LEFT, segment))
            self.event_queue.push(Event(segment.pt2, Event.RIGHT, segment))

    def run(self):
        while not self.event_queue.empty():
            event = self.event_queue.pop()
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
        self.sweep_line.insert(segment_e)   # Add segE to SL

        segment_above = self.sweep_line.successor(segment_e)    # Let segA = the segment Above segE in SL
        segment_below = self.sweep_line.predecessor(segment_e)  # Let segB = the segment Below segE in SL

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
        segment_above = self.sweep_line.successor(segment_e)  # Let segA = the segment Above segE in SL
        segment_below = self.sweep_line.predecessor(segment_e)  # Let segB = the segment Below segE in SL

        if segment_above and segment_below:     # if exists
            segment_above = segment_above.value     # get segment from node
            segment_below = segment_below.value     # get segment from node
            if segment_above.intersect(segment_below):    # If (I = Intersect( segA with segB) exists)
                return True

        self.sweep_line.remove(segment_e)
        return False
