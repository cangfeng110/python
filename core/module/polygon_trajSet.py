#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue June 23 11:40:11 2020

@author: uisee
"""
import sys
sys.path.append('../../')

import core.module.pos as pos_t
import core.module.polygon as polygon_t
import core.module.polygon_traj as polygon_traj_t

'one frame polgyon trajs'
class Polygon_TrajSet():
    def __init__(self):
        self.polygon_trajset = []

    def add_polygon_traj(self, polygon_traj):
        self.polygon_trajset.append(polygon_traj)

    def print_polygon_trajset(self):
        i = 0
        for polygon_traj in self.polygon_trajset:
            print('%dth polygon traj' % i)
            polygon_traj.print_polygon_traj()
            i+=1


if __name__ == '__main__':
    polygon_trajset = Polygon_TrajSet()

    polygon_traj = polygon_traj_t.Polygon_Traj()

    p = pos_t.Pos(0, 0)
    polygon = polygon_t.Polygon(p)
    vertex1 = pos_t.Pos(-1, 1)
    vertex2 = pos_t.Pos(-1, -1)
    vertex3 = pos_t.Pos(1, -1)
    vertex4 = pos_t.Pos(1, 1)
    polygon.add_vertex(vertex1)
    polygon.add_vertex(vertex2)
    polygon.add_vertex(vertex3)
    polygon.add_vertex(vertex4)
    polygon_traj.add_polygon(polygon)

    p = pos_t.Pos(0, 1)
    polygon = polygon_t.Polygon(p)
    vertex1 = pos_t.Pos(-1, 2)
    vertex2 = pos_t.Pos(-1, 0)
    vertex3 = pos_t.Pos(1, 0)
    vertex4 = pos_t.Pos(1, 2)
    polygon.add_vertex(vertex1)
    polygon.add_vertex(vertex2)
    polygon.add_vertex(vertex3)
    polygon.add_vertex(vertex4)
    polygon_traj.add_polygon(polygon)

    polygon_trajset.add_polygon_traj(polygon_traj)

    polygon_traj = polygon_traj_t.Polygon_Traj()

    p = pos_t.Pos(0, 0)
    polygon = polygon_t.Polygon(p)
    vertex1 = pos_t.Pos(-1, 1)
    vertex2 = pos_t.Pos(-1, -1)
    vertex3 = pos_t.Pos(1, -1)
    vertex4 = pos_t.Pos(1, 1)
    polygon.add_vertex(vertex1)
    polygon.add_vertex(vertex2)
    polygon.add_vertex(vertex3)
    polygon.add_vertex(vertex4)
    polygon_traj.add_polygon(polygon)

    p = pos_t.Pos(0, 1)
    polygon = polygon_t.Polygon(p)
    vertex1 = pos_t.Pos(-1, 2)
    vertex2 = pos_t.Pos(-1, 0)
    vertex3 = pos_t.Pos(1, 0)
    vertex4 = pos_t.Pos(1, 2)
    polygon.add_vertex(vertex1)
    polygon.add_vertex(vertex2)
    polygon.add_vertex(vertex3)
    polygon.add_vertex(vertex4)
    polygon_traj.add_polygon(polygon)

    polygon_trajset.add_polygon_traj(polygon_traj)

    polygon_trajset.print_polygon_trajset()
