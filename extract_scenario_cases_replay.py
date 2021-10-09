import math
import numpy as np
import argparse
import string
import re
import os
import json

class pred_scenario_data():
    def __init__(self):
        self.frame_idx = []
        self.obj_id = []
        self.scenario = []
        self.cnt = []
        return

    def parse_log_file(self, log_file):
        int_pattern = re.compile(r'(\d$)')
        pred_effect_pattern = re.compile(r'.*PRED_SCENARIO_CASE')
        with open(log_file, 'r') as log:
            line = log.readline()

            while line:
                line = line.rstrip('\n')
                match = pred_effect_pattern.match(line)
                if match:
                    line_split = line.split('CASE:')
                    data_list = line_split[1].split(',')

                    self.scenario.append(int(data_list[0]))
                    self.frame_idx.append(int(data_list[1]))
                    self.obj_id.append(int(data_list[2]))
                    self.cnt.append(int(data_list[3]))

                line = log.readline()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', action='store', dest='log_file', \
                        default="None", help='uos_local_planner.log')
    parser.add_argument('--log-path', action='store', dest='log_path', \
                        default="None", help='path containing logs and ucdfs')
    parser.add_argument('--ucdf', action='store', dest='ucdf_file', \
                        default="None", help='ucdf file')
    parser.add_argument('--run-path', action='store', dest='run_path', \
                        default="None", help='uos run path')
    parser.add_argument('--case-path', action='store', dest='case_path', \
                        default="None", help='path to store scenario cases')
    parser.add_argument('--scenario', action='store', dest='scenario', \
                        default=-1, help='path to store scenario cases')
    log_input = parser.parse_args()

    if not os.path.exists(log_input.log_file):
        print("Invalid log file!")
        return
    log_file = os.path.normpath(log_input.log_file)

    if not os.path.exists(log_input.log_path) or not os.path.isdir(log_input.log_path):
        print("Invalid log path!")
        return
    log_path = os.path.normpath(log_input.log_path)

    if not os.path.exists(log_input.ucdf_file):
        print("Invalid ucdf file!")
        return
    ucdf_file = os.path.normpath(log_input.ucdf_file)

    if not os.path.exists(log_input.run_path) or not os.path.isdir(log_input.run_path):
        print("Invalid run path!")
        return
    run_path = os.path.normpath(log_input.run_path)

    if not os.path.exists(log_input.case_path) or not os.path.isdir(log_input.case_path):
        print("Invalid case path!")
        return
    case_path = os.path.normpath(log_input.case_path)

    data = pred_scenario_data()
    data.parse_log_file(log_file)

    store_path = os.path.join(case_path, os.path.basename(log_path))
    cmd = "cd " + case_path + " && mkdir -p " + os.path.basename(log_path)
    os.system(cmd)

    # store hmap and rmap files
    cmd = "cd " + store_path + " && mkdir -p  map_files"
    os.system(cmd)
    cmd = "cp " + os.path.join(log_path, "map") + "/* " + \
        os.path.join(store_path, "map_files")
    os.system(cmd)

    # store uos_common.json and scenario case log
    cmd = "cd " + store_path + " && mkdir -p  log_files"
    os.system(cmd)
    cmd = "cp " + os.path.join(log_path, "uos_common.json") + " " + \
        os.path.join(store_path, "log_files")
    os.system(cmd)
    log_name = os.path.basename(ucdf_file).split(".")[0] + ".log"
    cmd = "cp " + log_file + " " + \
        os.path.join(store_path, os.path.join("log_files/" + log_name))
    os.system(cmd)

    for i in range(len(data.obj_id)):
        if int(log_input.scenario) != -1:
            if data.scenario[i] != int(log_input.scenario):
                continue

        print(data.scenario[i], data.obj_id[i])
        start_idx = np.max([data.frame_idx[i] - data.cnt[i] - 20, 0])
        end_idx = data.frame_idx[i] + 20
        cmd = "cd " + run_path + " && bin/uos_replay-trunc -f " + \
            ucdf_file + " -s " + str(start_idx) + " -e " + str(end_idx)
        os.system(cmd)

        scenario_case_dir = str(data.scenario[i]) + "_" + str(data.obj_id[i]) + \
            "_" + str(start_idx) + "-" + str(end_idx)
        cmd = "cd " + store_path + " && mkdir -p " + scenario_case_dir
        os.system(cmd)

        scenario_case_path = os.path.join(store_path, scenario_case_dir)
        trunc_ucdf_fname = os.path.basename(ucdf_file)
        trunc_ucdf_fname = trunc_ucdf_fname.split(".")[0] + "_" + \
            str(start_idx) + "-" + str(end_idx) + ".ucdf"
        trunc_ucdf_path = os.path.join(run_path, trunc_ucdf_fname)
        cmd = "mv " + trunc_ucdf_path + " " + scenario_case_path
        os.system(cmd)

        case_json_dict = {}
        case_json_dict["scenario"] = data.scenario[i]
        case_json_dict["obj_id"] = data.obj_id[i]
        case_json_dict["start_idx"] = int(start_idx)
        case_json_dict["end_idx"] = int(end_idx)
        case_json_dict["start_ts"] = -1
        case_json_dict["end_ts"] = -1
        case_json_fname = os.path.join(scenario_case_path, "case.json")
        file_obj = open(case_json_fname, 'w')
        if file_obj:
            json.dump(case_json_dict, file_obj, sort_keys=True, indent=4)
        else:
            raise ValueError("Failed to write to case.json!")

if __name__ == '__main__':
    main()
