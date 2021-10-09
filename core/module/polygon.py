#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue June 23 11:40:11 2020

@author: uisee
"""
import sys
sys.path.append('../../')

import core.module.pos as pos_t

'one polgyon'
class Polygon():
    def __init__(self, p):
        self.center_pt = p
        self.vertexes = []

    def add_vertex(self, vertex):
        self.vertexes.append(vertex)

    def print_polygon(self):
        print("center pt:(%.2f,%.2f)" % (self.center_pt.x, self.center_pt.y))
        print("vertexes:", end="")
        for p in self.vertexes:
            print("(%.2f,%.2f)" % (p.x, p.y), end="")
        print("")

if __name__ == '__main__':
    p = pos_t.Pos(0, 0)
    polygon = Polygon(p)
    vertex1 = pos_t.Pos(-1, 1)
    vertex2 = pos_t.Pos(-1, -1)
    vertex3 = pos_t.Pos(1, -1)
    vertex4 = pos_t.Pos(1, 1)
    polygon.add_vertex(vertex1)
    polygon.add_vertex(vertex2)
    polygon.add_vertex(vertex3)
    polygon.add_vertex(vertex4)
    polygon.print_polygon()
