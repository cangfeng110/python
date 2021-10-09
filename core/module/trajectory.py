#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue June 23 11:40:11 2020

@author: uisee
"""
import sys
sys.path.append('../../')

import core.module.pos as pos_t

'one trajectory'
class Trajectory():
    def __init__(self):
        self.pos_set = []

    def add_pos(self, p):
        self.pos_set.append(p)

    def print_traj(self):
        for p in self.pos_set:
            p.print_xy()

if __name__ == '__main__':
    traj = Trajectory()
    p = pos_t.Pos(0, 0)
    traj.add_pos(p)

    p = pos_t.Pos(1, 2)
    traj.add_pos(p)

    traj.print_traj()


