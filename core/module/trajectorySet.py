#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue June 23 11:40:11 2020

@author: uisee
"""

import sys
sys.path.append('../../')

import core.module.pos as pos_t
import core.module.trajectory as trajectory_t

class TrajectorySet:
    def __init__(self):
        self.traj_set = []

    def add_traj(self, traj):
        self.traj_set.append(traj)

    def print_traj_set(self):
        i = 0
        for traj in self.traj_set:
            print("====== print the %dth trajectory ======" % (i))
            traj.print_traj()
            i += 1

if __name__ == '__main__':
    trajSet = TrajectorySet()

    traj = trajectory_t.Trajectory()
    p = pos_t.Pos(0, 0)
    traj.add_pos(p)

    p = pos_t.Pos(1, 2)
    traj.add_pos(p)
    trajSet.add_traj(traj)

    traj = trajectory_t.Trajectory()
    p = pos_t.Pos(5, 5)
    traj.add_pos(p)

    p = pos_t.Pos(10, 10)
    traj.add_pos(p)
    trajSet.add_traj(traj)

    trajSet.print_traj_set()
