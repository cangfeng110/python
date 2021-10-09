import os
import sys
import json
import argparse
import re
import pandas as pd
import core.json_processor as json_processor
import pickle
import matplotlib.pyplot as plt

def check_junction_case_validity(case_path):
    annotation_found = False
    annotation_fname = ""
    obj_id = -1
    scenario = -1

    for fname in os.listdir(case_path):
        if fname.find("annotation") >= 0:
            annotation_fname = os.path.abspath(os.path.join(case_path, fname))
            annotation_found = True
        if fname == "case.json":
            json_file = os.path.abspath(os.path.join(case_path, fname))
            processor = json_processor.json_processor(json_file)
            json_dict = processor.read_json_as_dict()
            obj_id = json_dict["obj_id"]
            scenario = json_dict["scenario"]
    if not annotation_found:
        return False, annotation_fname, obj_id
    if obj_id < 0:
        return False, annotation_fname, obj_id
    if scenario != 1:
        return False, annotation_fname, obj_id

    return True, annotation_fname, obj_id

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-path", action="store", dest="case_path", default="None")
    parser.add_argument("--output-path", action="store", dest="output_path", default="None")
    log_input = parser.parse_args()

    if not os.path.exists(log_input.case_path):
        raise ValueError("Invalid case path!")
    if not os.path.exists(log_input.output_path):
        raise ValueError("Invalid output path!")

    case_path = os.path.abspath(log_input.case_path)
    output_path = os.path.abspath(log_input.output_path)

    data_df = pd.DataFrame()
    for root, dirs, files in os.walk(case_path, topdown=False):
        for item in dirs:
            one_case_path = os.path.abspath(os.path.join(root, item))
            valid, annotation_fname, _ = check_junction_case_validity(one_case_path)
            if not valid:
                continue

            data_df = data_df.append(pd.read_pickle(annotation_fname), \
                                     ignore_index=True)

    output_path = os.path.join(output_path, "junction_features.annotation")
    data_df.to_pickle(output_path)

    data_df.to_excel("/tmp/junction_feature_annotation.xlsx")

    fig, axs = plt.subplots(4)
    for i in range(4):
        axs[i].hist(data_df.iloc[:, i], bins=20)
    plt.show()

if __name__ == "__main__":
    main()
