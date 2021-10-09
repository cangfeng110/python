import math
import numpy as np
import argparse
import string
import re
import os
import json
import matplotlib.pyplot as plt
import core.feature_pb2 as feature_pb2
import core.common_pb2 as common_pb2
import core.json_processor as json_processor
from google.protobuf.internal.decoder import _DecodeVarint32
import pandas as pd
import pickle

def is_pt_in_poly(pt, poly):
    if len(poly) < 3:
        return False

    odd_intersection = False
    for i in range(len(poly)):
        if i == 0:
            j = len(poly) - 1
        else:
            j = i - 1
        x_1 = poly[i].x
        y_1 = poly[i].y
        x_2 = poly[j].x
        y_2 = poly[j].y

        if (pt.x == x_1 and pt.y == y_1) or (pt.x == x_2 and pt.y == y_2):
            return True

        if np.fabs(y_1 - y_2) > 0.0:
            if (y_1 < pt.y) != (y_2 < pt.y):
                x = (x_2 - x_1) * (pt.y - y_1) / (y_2 - y_1) + x_1
                if x == pt.x:
                    return True
                if pt.x < x:
                    odd_intersection = not odd_intersection

        elif y_1 == pt.y and y_2 == pt.y:
            if (pt.x <= x_1) != (pt.x <= x_2):
                return True

    return odd_intersection

def get_theta_diff(theta_1, theta_2):
    theta_diff = theta_2 - theta_1
    rem = np.fmod(theta_diff, 2.0 * np.pi)
    if theta_diff >= 0.0:
        theta_diff_cvt = rem
    else:
        if rem == 0.0:
            theta_diff_cvt = rem
        else:
            theta_diff_cvt = rem + 2.0 * np.pi

    return theta_diff_cvt

def get_obj_junction_exit(obj_pose, junction_exits, junction_vertices):
    res_idx = -1
    res_pose = common_pb2.Pose()
    min_dist = 1000000.0

    if is_pt_in_poly(obj_pose[-1].pos, junction_vertices):
        return res_pose, res_idx, np.sqrt(min_dist)

    traj_in_poly = False
    for pose in obj_pose:
        if is_pt_in_poly(pose.pos, junction_vertices):
            traj_in_poly = True
            break
    if not traj_in_poly:
        return res_pose, res_idx, np.sqrt(min_dist)

    exit_idx = -1
    to_exit_dist = np.zeros([len(junction_exits)])
    for exit_pose in junction_exits:
        exit_idx += 1
        tmp_min_dist = 1000000.0
        for pose in obj_pose:
            theta_diff = get_theta_diff(pose.theta, exit_pose.theta)
            if theta_diff > 45.0 * np.pi / 180.0 and \
               theta_diff < 315.0 * np.pi / 180.0:
                continue

            dist = np.square(pose.pos.x - exit_pose.pos.x) + \
                np.square(pose.pos.y - exit_pose.pos.y)
            if dist < tmp_min_dist:
                tmp_min_dist = dist

        if tmp_min_dist < min_dist:
            min_dist = tmp_min_dist
            res_pose = exit_pose
            res_idx = exit_idx

    return res_pose, res_idx, np.sqrt(min_dist)

def check_junction_case_validity(case_path):
    feature_file_found = False
    feature_fname = ""
    obj_id = -1
    scenario = -1

    for fname in os.listdir(case_path):
        if fname.find("features") >= 0:
            feature_fname = os.path.abspath(os.path.join(case_path, fname))
            feature_file_found = True
        if fname == "case.json":
            json_file = os.path.abspath(os.path.join(case_path, fname))
            processor = json_processor.json_processor(json_file)
            json_dict = processor.read_json_as_dict()
            obj_id = json_dict["obj_id"]
            scenario = json_dict["scenario"]
    if not feature_file_found:
        return False, feature_fname, obj_id
    if obj_id < 0:
        return False, feature_fname, obj_id
    if scenario != 1:
        return False, feature_fname, obj_id

    return True, feature_fname, obj_id

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case-path', action='store', dest='case_path', \
                        default="None", help='individual case path')
    log_input = parser.parse_args()

    if not os.path.exists(log_input.case_path):
        raise ValueError("Invalid case path!")
    case_path = os.path.abspath(log_input.case_path)

    valid, feature_fname, obj_id = check_junction_case_validity(case_path)
    if not valid:
        print("Not a valid junction scenario case!")
        return

    junction_id = -1
    junction_exits = []
    junction_vertices = []
    obj_entry = []
    obj_pose = []
    frame_idx = []
    cont_evidence = []
    causal_evidence = []
    cont_evidence_valid = []
    causal_evidence_valid = []
    dbn_cont_evidence_num = \
        feature_pb2.MotorJunctionDBNContEvidence.MOTOR_JUNCTION_DBN_CONT_EVIDENCE_NUM
    dbn_causal_evidence_num = \
        feature_pb2.MotorJunctionDBNCausalEvidence.MOTOR_JUNCTION_DBN_CAUSAL_EVIDENCE_NUM

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

                obj_pose.append(feature.obj_pose)
                frame_idx.append(features.frame_idx)

                if not feature.HasField("motor_junction_feature"):
                    continue

                junction = feature.motor_junction_feature.junction
                curr_junction_id = junction.junction_id
                junction_feature = feature.motor_junction_feature
                if junction_id == -1:
                    junction_id = curr_junction_id
                    obj_entry.append(junction_feature.obj_entry)
                    for exit_pose in junction.junction_exits:
                        junction_exits.append(exit_pose)
                    for vertex in junction.vertices:
                        junction_vertices.append(vertex)

                # only consider the first junction encountered
                if junction_id != -1 and curr_junction_id != junction_id:
                    break

                cont_evidence.append(junction_feature.motor_veh_dbn_cont_evidence)
                causal_evidence.append(junction_feature.motor_veh_dbn_causal_evidence)
                cont_evidence_valid.append(junction_feature.dbn_cont_evidence_valid)
                causal_evidence_valid.append(junction_feature.dbn_causal_evidence_valid)

    if junction_id < 0 or len(obj_pose) <= 0:
        print("No junction traj is found!")
        return

    obj_junction_exit, obj_exit_idx, exit_dist = \
        get_obj_junction_exit(obj_pose, junction_exits, junction_vertices)
    if obj_exit_idx < 0:
        print("Cannot find correct exit!")
        return
    if exit_dist > 10.0:
        print("Exit dist is {:.3f}m. Junction roadmap may not be correct!".format(exit_dist))
        return

    annotated_cont_evidence = np.zeros([len(cont_evidence), dbn_cont_evidence_num])
    annotated_causal_evidence = np.zeros([len(causal_evidence), dbn_causal_evidence_num])
    annotated_class = np.zeros([len(cont_evidence), 1])
    annotated_junction_id = np.zeros([len(cont_evidence), 1])
    annotated_junction_exit_id = np.zeros([len(cont_evidence), 1])
    for i in range(len(cont_evidence)):
        annotated_class[i, 0] = 1.0
        annotated_junction_id[i, 0] = junction_id
        annotated_junction_exit_id[i, 0] = obj_exit_idx

        evidence = cont_evidence[i]
        valid = cont_evidence_valid[i]
        for j in range(dbn_cont_evidence_num):
            if valid[obj_exit_idx * dbn_cont_evidence_num + j]:
                annotated_cont_evidence[i, j] = \
                    evidence[obj_exit_idx * dbn_cont_evidence_num + j]
            else:
                annotated_cont_evidence[i, j] = np.NaN

        evidence = causal_evidence[i]
        valid = causal_evidence_valid[i]
        for j in range(dbn_causal_evidence_num):
            if valid[obj_exit_idx * dbn_causal_evidence_num + j]:
                annotated_causal_evidence[i, j] = \
                    bool(evidence[obj_exit_idx * dbn_causal_evidence_num + j])
            else:
                annotated_causal_evidence[i, j] = np.NaN

    annotation_data_array = np.concatenate([annotated_cont_evidence, \
                                            annotated_causal_evidence, \
                                            annotated_class, \
                                            annotated_junction_id, \
                                            annotated_junction_exit_id], axis=1)

    evidence_labels = []
    for i in range(dbn_cont_evidence_num):
        evidence_labels.append(feature_pb2.MotorJunctionDBNContEvidence.Name(i))
    for i in range(dbn_causal_evidence_num):
        evidence_labels.append(feature_pb2.MotorJunctionDBNCausalEvidence.Name(i))

    annotation_data = pd.DataFrame(data=annotation_data_array, \
                                   columns=evidence_labels + \
                                   ['class_label', 'junction_id', 'exit_id'])

    output_path = os.path.join(os.path.dirname(feature_fname), \
                               os.path.basename(feature_fname.replace("features", "annotation")))
    annotation_data.to_pickle(output_path)

if __name__ == '__main__':
    main()
