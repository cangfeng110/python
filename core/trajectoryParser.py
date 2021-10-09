#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue June 23 11:40:11 2020

@author: uisee
"""
import sys
sys.path.append('../')

import re
import math
import argparse
import core.module.pos as pos_t
import core.module.trajectory as trajectory_t
import core.module.trajectorySet as trajectory_set_t
import core.module.trajectorySetSet as trajectorySetSet_t

def parser_options():
    parser = argparse.ArgumentParser()
    # save png, save(0), not (1)
    parser.add_argument('--s', type=int, nargs='?', dest='if_save_fig',
                        help='input 0 or 1', default=0)
    # case path
    parser.add_argument('--p', type=str, nargs='?', dest='case_path',
                        help='case path', default='case')

    parser.add_argument('--log1', action='store', dest='log_file1',
                        default="/home/uisee/uos/install/data/log/uos_local_planner.log",
                        help='uos_local_planner.log')

    parser.add_argument('--log2', action='store', dest='log_file2',
                        default="/home/uisee/uos/install/data/log/uos_planner.log",
                        help='uos_planner.log')
    global log_input
    log_input = parser.parse_args()

    if_save_fig = parser.parse_args().if_save_fig
    if if_save_fig != 0 and if_save_fig != 1:
        print("Error: The params 's' must be 0 or 1!")
        sys.exit(0)

class ParseLogFile():
    def __init__(self, log1_name, log2_name):
        self.file1_name = log1_name
        self.file2_name = log2_name

    def parse_frame_idx(self):
        ucdf_idxes = []
        with open(self.file1_name, 'r') as log:
            line_pattern = re.compile(r'.*TRAJ_TRUE_EVAL')

            line = log.readline()
            while line:
                line = line.rstrip('\n')
                match = line_pattern.match(line)
                if match:
                    line_split = line.split(":[")
                    line_split[1] = line_split[1].rstrip("]")
                    data = line_split[1].split(",")
                    ucdf_idx = int(data[0])
                    ucdf_idxes.append(ucdf_idx)
                line = log.readline()

        if len(ucdf_idxes) <= 0:
            print("Error: lost ucdf idx indf!")

        return ucdf_idxes

    def parse_ucdf_timestamps(self):
        ucdf_ts = []
        with open(self.file2_name, 'r') as log:

            line_pattern = re.compile(r'.*UCDF_TS')
            line = log.readline()
            while line:
                line = line.rstrip('\n')
                match = line_pattern.match(line)
                if match:
                    line_split = line.split(":[")
                    data = line_split[1].rstrip("]")
                    ts = float(data) / 1e6
                    ucdf_ts.append(ts)
                line = log.readline()

        if len(ucdf_ts) <= 0:
            print("Error: lost timestamp info!")
            sys.exit(1)

        return ucdf_ts

    def parse_true_traj(self):
        traj = trajectory_t.Trajectory()
        with open(self.file1_name, 'r') as log:
            line_pattern = re.compile(r'.*TRAJ_TRUE_EVAL')

            line = log.readline()
            while line:
                line = line.rstrip('\n')
                match = line_pattern.match(line)
                if match:
                    line_split = line.split(":[")
                    line_split[1] = line_split[1].rstrip("]")
                    data = line_split[1].split(",")
                    p = pos_t.Pos(float(data[1]), float(data[2]))
                    p.theta = (math.pi / 2.0 - float(data[3]))
                    traj.add_pos(p)
                line = log.readline()

        if len(traj.pos_set) <= 0:
            print("Error: lost true traj info!")
            sys.exit(1)

        return traj

    def parse_pred_trajSet_set(self):
        trajSet_set = trajectorySetSet_t.TrajectorySetSet()
        with open(self.file1_name, 'r') as log:
            true_traj_pattern = re.compile(r'.*TRAJ_TRUE_EVAL')
            pred_traj_pattern = re.compile(r'.*TRAJ_PRED_EVAL')
            pred_traj_num_pattern = re.compile(r'.*TRAJ_PRED_NUM')

            frame_idx = ''
            traj_idx = ''

            line = log.readline()
            while line:
                line = line.rstrip('\n')

                match = true_traj_pattern.match(line)
                if match:
                    line_split = line.split(":[")
                    line_split[1] = line_split[1].rstrip("]")
                    data = line_split[1].split(",")
                    if frame_idx != '':
                        traj_set.add_traj(traj)
                        trajSet_set.add_trajSet(traj_set)

                    traj_set = trajectory_set_t.TrajectorySet()
                    frame_idx = data[0]

                match = pred_traj_pattern.match(line)
                if match:
                    line_split = line.split(":[")
                    line_split[1] = line_split[1].rstrip("]")
                    data = line_split[1].split(",")
                    p = pos_t.Pos(float(data[0]), float(data[1]))
                    traj.add_pos(p)

                match = pred_traj_num_pattern.match(line)
                if match:
                    line_split = line.split(":[")
                    line_split[1] = line_split[1].rstrip("]")
                    data = line_split[1].split(",")

                    if traj_idx != '' and data[0] != '0':
                        traj_set.add_traj(traj)
                    traj = trajectory_t.Trajectory()
                    traj_idx = data[0]

                line = log.readline()

            if 'traj' in dir():
                traj_set.add_traj(traj)
            else:
                print("Error: lost pred traj info!")
                sys.exit(1)

            if 'traj_set' in dir():
                trajSet_set.add_trajSet(traj_set)
            else:
                print("Error: lost pred traj info!")
                sys.exit(1)
        if len(trajSet_set.trajSet_set) <= 0:
            print("Error: lost pred traj info!")
            sys.exit(1)

        return trajSet_set

    def parse_data(self):
        true_traj = self.parse_true_traj()
        pred_trajSet_set = self.parse_pred_trajSet_set()
        ucdf_idxes = self.parse_frame_idx()
        ucdf_ts = self.parse_ucdf_timestamps()
        if len(ucdf_ts) < len(ucdf_idxes):
            print("Error: timestamps size can't smaller than true traj size!")
            sys,exit(1)
        #ucdf_ts = ucdf_ts[ucdf_idxes[0]:ucdf_idxes[-1] + 1]

        return true_traj, pred_trajSet_set, ucdf_idxes, ucdf_ts


if __name__ == '__main__':
    parser_options()
    parseLogFile = ParseLogFile(log_input.log_file1, log_input.log_file2)

    true_traj, pred_trajSet_set, ucdf_idxes, ucdf_ts = parseLogFile.parse_data()
    print("\n ====== ucdf frame idx ======")
    print(ucdf_idxes)
    print("\n ====== timestamps size %d ======" % (len(ucdf_ts)))
    print(ucdf_ts)
    print("\n ====== true traj size %d ======" % (len(true_traj.pos_set)))
    true_traj.print_traj()

    pred_trajSet_set.print_trajSet_set()
