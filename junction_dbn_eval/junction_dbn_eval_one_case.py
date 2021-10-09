import math
import numpy as np
import argparse
import string
import re
import os
import json
import sys
sys.path.append('..')
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
    obj_id = -1
    scenario = -1

    for fname in os.listdir(case_path):
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
    if not annotation_file_found:
        return False, annotation_fname, pred_output_fname, obj_id
    if not pred_output_found:
        return False, annotation_fname, pred_output_fname, obj_id
    if obj_id < 0:
        return False, annotation_fname, pred_output_fname, obj_id
    if scenario != 1:
        return False, annotation_fname, pred_output_fname, obj_id

    return True, annotation_fname, pred_output_fname, obj_id

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case-path', action='store', dest='case_path', \
                        default="None", help='individual case path')
    log_input = parser.parse_args()

    if not os.path.exists(log_input.case_path):
        raise ValueError("Invalid case path!")
    case_path = os.path.abspath(log_input.case_path)

    valid, annotation_fname, pred_output_fname, obj_id = \
        check_junction_case_validity(case_path)
    if not valid:
        print("Not a valid junction scenario case!")
        return

    junction_id = -1
    frame_idx = []
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
                if junction_id == -1:
                    junction_id = curr_junction_id

                # only consider the first junction encountered
                if junction_id != -1 and curr_junction_id != junction_id:
                    break

                exit_probs.append(junction_pred_res.exit_probs)
                frame_idx.append(pred_output.frame_idx)

    if junction_id < 0 or len(frame_idx) <= 0:
        print("No junction pred result is found!")
        return

    annotation_data = pd.read_pickle(annotation_fname)
    exit_idx = int(annotation_data["exit_id"].iloc[0])
    junction_id = int(annotation_data["junction_id"].iloc[0])

    if (len(frame_idx) > 0):
        res = 0.0
        for i in range(len(frame_idx)):
            res = res + np.square(1.0 - exit_probs[i][exit_idx])
        res = res / len(frame_idx)
    else:
        res = 1.0

    res_data = pd.DataFrame(columns=["mean_brier_score", "junction_id", "exit_idx"])
    res_data.loc[-1] = [res, junction_id, exit_idx]
    output_path = os.path.join(os.path.dirname(pred_output_fname), \
                               "junction_exit.brier_score")
    res_data.to_pickle(output_path)
    print("Mean brier score is {:.3f}.".format(res))

if __name__ == '__main__':
    main()
