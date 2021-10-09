import os
import sys
import json
import argparse
import re
import pandas as pd
sys.path.append('..')
import core.json_processor as json_processor
import pickle
import matplotlib.pyplot as plt

def check_junction_case_validity(case_path):
    dbn_eval_res_found = False
    dbn_eval_res_fname = ""
    traj_eval_res_found = False
    traj_eval_res_fname = ""
    obj_id = -1
    scenario = -1

    for fname in os.listdir(case_path):
        if fname.find("traj_eval_res") >= 0:
            traj_eval_res_fname = os.path.abspath(os.path.join(case_path, fname))
            traj_eval_res_found = True
        if fname.find("brier_score") >= 0:
            dbn_eval_res_fname = os.path.abspath(os.path.join(case_path, fname))
            dbn_eval_res_found = True
        if fname == "case.json":
            json_file = os.path.abspath(os.path.join(case_path, fname))
            processor = json_processor.json_processor(json_file)
            json_dict = processor.read_json_as_dict()
            obj_id = json_dict["obj_id"]
            scenario = json_dict["scenario"]
    if not dbn_eval_res_found:
        return False, dbn_eval_res_fname, traj_eval_res_fname, obj_id
    if not traj_eval_res_found:
        return False, dbn_eval_res_fname, traj_eval_res_fname, obj_id
    if obj_id < 0:
        return False, dbn_eval_res_fname, traj_eval_res_fname, obj_id
    if scenario != 1:
        return False, dbn_eval_res_fname, traj_eval_res_fname, obj_id

    return True, dbn_eval_res_fname, traj_eval_res_fname, obj_id

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
    column_labels = ['case_path', 'mean_brier_score', 'ave_pos_err', 'end_ave_pos_err', \
                     'junction_id', 'exit_idx']
    for root, dirs, files in os.walk(case_path, topdown=False):
        for item in dirs:
            one_case_path = os.path.abspath(os.path.join(root, item))
            valid, dbn_eval_res_fname, traj_eval_res_fname, _ = \
                check_junction_case_validity(one_case_path)
            if not valid:
                continue

            res_df = pd.DataFrame(columns=column_labels)
            res_df.loc[-1] = [one_case_path, \
                              pd.read_pickle(dbn_eval_res_fname)['mean_brier_score'].iloc[0], \
                              pd.read_pickle(traj_eval_res_fname)['ave_pos_err'].iloc[0], \
                              pd.read_pickle(traj_eval_res_fname)['end_ave_pos_err'].iloc[0], \
                              pd.read_pickle(dbn_eval_res_fname)['junction_id'].iloc[0], \
                              pd.read_pickle(dbn_eval_res_fname)['exit_idx'].iloc[0]]
            data_df = data_df.append(res_df, ignore_index=True)

    output_path = os.path.join(output_path, "junction.eval_res")
    data_df.to_pickle(output_path)

    data_df.to_excel("/tmp/junction_eval_res.xlsx")

if __name__ == "__main__":
    main()
