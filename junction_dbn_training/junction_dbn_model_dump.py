import json
import os
import math
import numpy as np
import argparse
import string
import sys
sys.path.append('..')
import core.motor_junction_dbn_model_pb2 as motor_junction_dbn_model_pb2

def parser_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-json', action='store', dest='model_json', \
                        default="/tmp/test.json", help='model_json')
    parser.add_argument('--output-path', action='store', dest='output_path', \
                        default="/tmp/", help='path for outputting model')

    global log_input
    log_input = parser.parse_args()

def main():
    parser_options()
    if os.path.exists(log_input.model_json):
        param_object = open(log_input.model_json, 'r')
        param_dict = json.load(param_object)
    else:
        raise ValueError("Invalid param json!")

    if not os.path.exists(log_input.output_path):
        raise ValueError("Invalid output_path!")

    model = motor_junction_dbn_model_pb2.MotorJunctionDBNModel()

    for evidence in param_dict["continuous_evidence"]:
        num = len(param_dict["continuous_evidence_interval"][evidence])
        if num > 0:
            model.continuous_evidence_interval_num.append(num-1)
            model.evidence_interval.extend(
                param_dict["continuous_evidence_interval"][evidence])

    if len(param_dict["intention_switching_prob"]) > 0:
        model.ispt.extend(param_dict["intention_switching_prob"])

    if len(param_dict["intention_evidence_relation"]) > 0:
        model.iert.extend(param_dict["intention_evidence_relation"])

    for evidence in param_dict["continuous_evidence"]:
        num = len(param_dict["cpt"][evidence])
        if num > 0:
            model.cpt.extend(param_dict["cpt"][evidence])
    for evidence in param_dict["binary_evidence"]:
        num = len(param_dict["cpt"][evidence])
        if num > 0:
            model.cpt.extend(param_dict["cpt"][evidence])
    for evidence in param_dict["causal_evidence"]:
        num = len(param_dict["cpt"][evidence])
        if num > 0:
            model.cpt.extend(param_dict["cpt"][evidence])

    model.prior_sample_size = param_dict["prior_sample_size"]

    for name in param_dict["continuous_evidence"]:
        model.continuous_evidence.extend(name)
    for name in param_dict["binary_evidence"]:
        model.binary_evidence.extend(name)
    for name in param_dict["causal_evidence"]:
        model.causal_evidence.extend(name)

    f = open(os.path.join(log_input.output_path, "motor_junction_dbn_model.bin"), "wb")
    f.write(model.SerializeToString())
    f.close()

if __name__ == '__main__':
    main()
