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
    log_input = parser.parse_args()

    if not os.path.exists(log_input.case_path):
        raise ValueError("Invalid case path!")
    case_path = os.path.abspath(log_input.case_path)

    valid, feature_fname, annotation_fname, pred_output_fname, obj_id = \
        check_junction_case_validity(case_path)
    if not valid:
        print("Not a valid junction scenario case!")
        return

    junction_id_1 = -1
    frame_idx_1 = []
    exit_probs = []
    with open(pred_output_fname, 'rb') as f:
        buf = f.read()
        n = 0
        while n < len(buf):
            msg_len, new_pos = _DecodeVarint32(buf, n)
            n = new_pos
            msg_buf = buf[n : n + msg_len]
            n += msg_len
            pred_output = prediction_output_pb2.PredictionOutput()
            pred_output.ParseFromString(msg_buf)

            for pred_result in pred_output.pred_results:
                if pred_result.obj_id != obj_id:
                    continue
                if not pred_result.HasField("junction_pred_result"):
                    continue

                junction_pred_res = pred_result.junction_pred_result
                curr_junction_id = junction_pred_res.junction_id
                if junction_id_1 == -1:
                    junction_id_1 = curr_junction_id

                # only consider the first junction encountered
                if junction_id_1 != -1 and curr_junction_id != junction_id_1:
                    break

                exit_probs.append(junction_pred_res.exit_probs)
                frame_idx_1.append(pred_output.frame_idx)

    if junction_id_1 < 0 or len(frame_idx_1) <= 0:
        print("No junction pred result is found!")
        return

    junction_id_2 = -1
    junction_exits = []
    junction_vertices = []
    obj_entry = []
    obj_pose = []
    frame_idx_2 = []
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
                if junction_id_2 == -1:
                    junction_id_2 = curr_junction_id
                    obj_entry.append(junction_feature.obj_entry)
                    for exit_pose in junction.junction_exits:
                        junction_exits.append(exit_pose)
                    for vertex in junction.vertices:
                        junction_vertices.append(vertex)

                # only consider the first junction encountered
                if junction_id_2 != -1 and curr_junction_id != junction_id_2:
                    break

                obj_pose.append(feature.obj_pose)
                frame_idx_2.append(features.frame_idx)

    if junction_id_2 < 0 or len(obj_pose) <= 0:
        print("No junction traj is found!")
        return
    """
    if junction_id_1 != junction_id_2:
        print("Not the same junction!")
        return
    """

    annotation_data = pd.read_pickle(annotation_fname)
    exit_idx = int(annotation_data["exit_id"].iloc[0])
    junction_id = int(annotation_data["junction_id"].iloc[0])
    obj_junction_exit = junction_exits[exit_idx]

    fig, axs = plt.subplots(2,1)
    for i in range(len(junction_exits)):
        axs[0].scatter(junction_exits[i].pos.x, junction_exits[i].pos.y, color='r')
        axs[0].arrow(junction_exits[i].pos.x, junction_exits[i].pos.y, \
                  np.cos(junction_exits[i].theta) * 2.0, \
                  np.sin(junction_exits[i].theta) * 2.0)
    for i in range(len(junction_vertices)):
        axs[0].plot([junction_vertices[i].x, junction_vertices[(i+1)%len(junction_vertices)].x], \
                 [junction_vertices[i].y, junction_vertices[(i+1)%len(junction_vertices)].y], \
                 color='b')
    for i in range(len(obj_pose)):
        axs[0].plot(obj_pose[i].pos.x, obj_pose[i].pos.y, color='g', marker='o', \
                 alpha=i/len(obj_pose))
    axs[0].scatter(obj_junction_exit.pos.x, obj_junction_exit.pos.y, \
                   color='r', marker='x', s=100)
    axs[0].scatter(obj_entry[0].pos.x, obj_entry[0].pos.y, \
                   color='g', marker='^', s=100)
    axs[0].axis('equal')

    annotated_exit_prob = np.zeros([len(exit_probs)])
    for i in range(len(exit_probs)):
        annotated_exit_prob[i] = exit_probs[i][exit_idx]
    axs[1].plot(annotated_exit_prob)
    axs[1].set_xlabel("frame")
    axs[1].set_ylabel("prob")

    plt.show()


if __name__ == '__main__':
    main()
