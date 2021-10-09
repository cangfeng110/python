import math
import numpy as np
import argparse
import string
import re
import os
import json
import matplotlib.pyplot as plt
import sys
sys.path.append('..')
import core.feature_pb2 as feature_pb2
import core.prediction_output_pb2 as prediction_output_pb2
import core.json_processor as json_processor
from google.protobuf.internal.decoder import _DecodeVarint32
import pandas as pd
import pickle

def check_junction_case_validity(case_path):
    annotation_file_found = False
    annotation_fname = ""
    pred_output_found = False
    pred_output_fname = ""
    feature_file_found = False
    feature_fname = ""
    obj_id = -1
    scenario = -1

    for fname in os.listdir(case_path):
        if fname.find("features") >= 0:
            feature_fname = os.path.abspath(os.path.join(case_path, fname))
            feature_file_found = True
        if fname.find("annotation") >= 0:
            annotation_fname = os.path.abspath(os.path.join(case_path, fname))
            annotation_file_found = True
        if fname.find("pred_output") >= 0:
            pred_output_fname = os.path.abspath(os.path.join(case_path, fname))
            pred_output_found = True
        if fname == "case.json":
            json_file = os.path.abspath(os.path.join(case_path, fname))
            processor = json_processor.json_processor(json_file)
            json_dict = processor.read_json_as_dict()
            obj_id = json_dict["obj_id"]
            scenario = json_dict["scenario"]
    if not feature_file_found:
        return False, feature_fname, annotation_fname, pred_output_fname, obj_id
    if not annotation_file_found:
        return False, feature_fname, annotation_fname, pred_output_fname, obj_id
    if not pred_output_found:
        return False, feature_fname, annotation_fname, pred_output_fname, obj_id
    if obj_id < 0:
        return False, feature_fname, annotation_fname, pred_output_fname, obj_id
    if scenario != 1:
        return False, feature_fname, annotation_fname, pred_output_fname, obj_id

    return True, feature_fname, annotation_fname, pred_output_fname, obj_id

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case-path', action='store', dest='case_path', \
                        default="None", help='individual case path')
    parser.add_argument('--junction-id', action='store', dest='junction_id', \
                        default=-1, help='junction id')
    log_input = parser.parse_args()

    if not os.path.exists(log_input.case_path):
        raise ValueError("Invalid case path!")
    case_path = os.path.abspath(log_input.case_path)

    input_junction_id = int(log_input.junction_id)

    obj_entry_set = []
    obj_exit_set = []
    obj_pose_set = []
    junction_exits = []
    junction_entries = []
    junction_vertices = []
    for root, dirs, files in os.walk(case_path, topdown=False):
        for item in dirs:
            one_case_path = os.path.abspath(os.path.join(root, item))

            valid, feature_fname, annotation_fname, pred_output_fname, obj_id = \
                check_junction_case_validity(one_case_path)
            if not valid:
                continue

            annotation_data = pd.read_pickle(annotation_fname)
            exit_idx = int(annotation_data["exit_id"].iloc[0])
            junction_id = int(annotation_data["junction_id"].iloc[0])

            if junction_id != input_junction_id:
                continue

            obj_entry = []
            obj_pose = []
            with open(feature_fname, 'rb') as f:
                buf = f.read()
                n = 0
                while n < len(buf):
                    msg_len, new_pos = _DecodeVarint32(buf, n)
                    n = new_pos
                    msg_buf = buf[n : n + msg_len]
                    n += msg_len
                    features = feature_pb2.Features()
                    features.ParseFromString(msg_buf)

                    for feature in features.features:
                        if feature.obj_id != obj_id:
                            continue
                        if not feature.HasField("motor_junction_feature"):
                            continue

                        junction = feature.motor_junction_feature.junction
                        curr_junction_id = junction.junction_id
                        junction_feature = feature.motor_junction_feature

                        # only consider the first junction encountered
                        if curr_junction_id != input_junction_id:
                            break

                        if 0 == len(junction_exits) and 0 == len(junction_vertices) \
                           and 0 == len(junction_entries):
                            obj_entry.append(junction_feature.obj_entry)
                            for exit_pose in junction.junction_exits:
                                junction_exits.append(exit_pose)
                            for entry_pose in junction.junction_entrys:
                                junction_entries.append(entry_pose)
                            for vertex in junction.vertices:
                                junction_vertices.append(vertex)
                        if 0 == len(obj_entry):
                            obj_entry.append(junction_feature.obj_entry)

                        obj_pose.append(feature.obj_pose)

            if len(obj_pose) <= 0:
                print("No junction traj is found!")
                continue
            else:
                obj_entry_set.append(obj_entry)
                obj_pose_set.append(obj_pose)
            if len(junction_exits) != 0:
                obj_exit_set.append(junction_exits[exit_idx])

    for j in range(len(obj_pose_set)):
        obj_pose = obj_pose_set[j]
        for i in range(len(obj_pose)):
            plt.plot(obj_pose[i].pos.x, obj_pose[i].pos.y, color='g', marker='o', \
                     alpha=i/len(obj_pose), zorder=1)
        """
        plt.scatter(obj_exit_set[j].pos.x, obj_exit_set[j].pos.y, \
                    color='r', marker='x', s=100)
        plt.scatter(obj_entry_set[j][0].pos.x, obj_entry_set[j][0].pos.y, \
                    color='g', marker='^', s=100)
        """
    for i in range(len(junction_exits)):
        plt.scatter(junction_exits[i].pos.x, junction_exits[i].pos.y, \
                    color='r', zorder=2, label='junction_exits')
        plt.arrow(junction_exits[i].pos.x, junction_exits[i].pos.y, \
                  np.cos(junction_exits[i].theta) * 2.0, \
                  np.sin(junction_exits[i].theta) * 2.0, zorder=2)
    for i in range(len(junction_entries)):
        plt.scatter(junction_entries[i].pos.x, junction_entries[i].pos.y, \
                    color='b', zorder=2, label='junction_entries')
        plt.arrow(junction_entries[i].pos.x, junction_entries[i].pos.y, \
                  np.cos(junction_entries[i].theta) * 2.0, \
                  np.sin(junction_entries[i].theta) * 2.0, zorder=2)
    for i in range(len(junction_vertices)):
        plt.plot([junction_vertices[i].x, junction_vertices[(i+1)%len(junction_vertices)].x], \
                 [junction_vertices[i].y, junction_vertices[(i+1)%len(junction_vertices)].y], \
                 color='y', zorder=0)

    plt.axis('equal')
    plt.show()


if __name__ == '__main__':
    main()
