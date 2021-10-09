#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue June 23 11:40:11 2020

@author: uisee
"""

class Pos():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.theta = 0.0

    def print_xy(self):
        print(" x,y,theta: ({:.2f},{:.2f},{:.2f})".format(self.x, self.y, self.theta))

if __name__ == '__main__':
    p = Pos(1.0, 1.0)
    p.theta = 3.14
    p.print_xy()
