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
import core.module.polygon_trajSet as polygon_trajSet_t

'all polygon trajs'
class Polygon_TrajSetSet():
    def __init__(self):
        self.polygon_trajsetset = []

    def add_polygon_trajSet(self, polygon_trajset):
        self.polygon_trajsetset.append(polygon_trajset)

    def print_polygon_trajsetset(self):
        i = 0
        for polygon_trajset in self.polygon_trajsetset:
            print('%dth frame trajs' % i)
            polygon_trajset.print_polygon_trajset()
            i+=1
            print("")

if __name__ == '__main__':
    polygon_trajsetset = Polygon_TrajSetSet()

    polygon_trajset = polygon_trajSet_t.Polygon_TrajSet()
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

    polygon_trajsetset.add_polygon_trajSet(polygon_trajset)

    polygon_trajset = polygon_trajSet_t.Polygon_TrajSet()
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

    polygon_trajsetset.add_polygon_trajSet(polygon_trajset)

    polygon_trajsetset.print_polygon_trajsetset()
