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
import core.module.trajectorySet as trajectorySet_t

class TrajectorySetSet:
    def __init__(self):
        self.trajSet_set = []

    def add_trajSet(self, traj_set):
        self.trajSet_set.append(traj_set)

    def print_trajSet_set(self):
        i = 0
        for traj_set in self.trajSet_set:
            print("\n ====== the %dth frame traj set ======\n" % (i))
            traj_set.print_traj_set()
            i += 1

if __name__ == '__main__':
    trajset_set = TrajectorySetSet()

    trajSet = trajectorySet_t.TrajectorySet()
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
    trajset_set.add_trajSet(trajSet)

    trajSet = trajectorySet_t.TrajectorySet()
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
    trajset_set.add_trajSet(trajSet)

    trajset_set.print_trajSet_set()
