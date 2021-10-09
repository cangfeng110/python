import os
import sys
import json
import argparse
import re
import core.json_processor as json_processor

redundant_mod_keys = ["_MOD_uos_camera", "_MOD_uos_chassis_ctrl", \
                      "_MOD_uos_compass", "_MOD_uos_cv_framework", \
                      "_MOD_uos_gps", "_MOD_uos_hawkeye", "_MOD_uos_io", \
                      "_MOD_uos_lslam_carto", "_MOD_uos_lidar", \
                      "_MOD_uos_lidar_framework", "_MOD_uos_mot", \
                      "_MOD_uos_navigation", "_MOD_uos_sick", \
                      "_MOD_uos_sonic", "_MOD_uos_rcs"]

def prepare(json_file, ucpf_fname_list):
    processor = json_processor.json_processor(json_file)
    for redundant_key in redundant_mod_keys:
        processor.del_key_val_in_json(redundant_key)

    processor.insert_key_val_to_json(["_MOD_uos_config", "run_scene"], "replay")
    processor.insert_key_val_to_json(["_MOD_uos_config", "platform"], "SMP")
    processor.insert_key_val_to_json(["_MOD_uos_local_planner", \
                                      "output_pred_scenario_case_log"], 0)
    processor.insert_key_val_to_json(["_MOD_uos_local_planner", \
                                      "dump_ucpf"], 0)
    processor.insert_key_val_to_json(["_MOD_uos_local_planner", \
                                      "prediction_replay"], 1)
    processor.insert_key_val_to_json(["_MOD_uos_local_planner", \
                                      "prediction_replay_ucpf_fname"], \
                                     ucpf_fname_list)
    processor.insert_key_val_to_json(["_MOD_uos_local_planner", \
                                      "dump_prediction_features"], 1)
    processor.insert_key_val_to_json(["_MOD_uos_local_planner", \
                                      "dump_motor_veh_junction_dbn_features"], 1)
    processor.del_key_val_in_json("st_decision")

    roadmap_fname = processor.find_key_val_in_json('roadmap_fname')[1]
    if roadmap_fname != "":
        roadmap = roadmap_fname.split('/')[-1]
        processor.insert_key_val_to_json(["_MOD_uos_local_planner", \
                                          "prediction_replay_rmap_fname"], \
                                         "data/" + roadmap)
    else:
        raise ValueError("roadmap is not found in uos_common.json!")

def check_junction_case_validity(case_path):
    ucpf_found = False
    ucpf_fname = ""
    obj_id = -1
    scenario = -1

    for fname in os.listdir(case_path):
        if fname == "test.ucpf":
            ucpf_fname = os.path.abspath(os.path.join(case_path, fname))
            ucpf_found = True
        if fname == "case.json":
            json_file = os.path.abspath(os.path.join(case_path, fname))
            processor = json_processor.json_processor(json_file)
            json_dict = processor.read_json_as_dict()
            obj_id = json_dict["obj_id"]
            scenario = json_dict["scenario"]
    if not ucpf_found:
        return False, ucpf_fname, obj_id
    if obj_id < 0:
        return False, ucpf_fname, obj_id
    if scenario != 1:
        return False, ucpf_fname, obj_id

    return True, ucpf_fname, obj_id

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-path", action="store", dest="case_path", default="None")
    parser.add_argument('--run-path', action='store', dest='run_path', default="None")
    parser.add_argument("--map-path", action="store", dest="map_path", default="None")
    parser.add_argument("--config", action="store", dest="config_file", default="None")
    log_input = parser.parse_args()

    if not os.path.exists(log_input.case_path):
        raise ValueError("Invalid case path!")
    if not os.path.exists(log_input.run_path):
        raise ValueError("Invalid run path!")
    if not os.path.exists(log_input.map_path):
        raise ValueError("Invalid map path!")
    if not os.path.exists(log_input.config_file):
        raise ValueError("Invalid config file!")

    run_path = os.path.abspath(log_input.run_path)
    case_path = os.path.abspath(log_input.case_path)
    map_path = os.path.abspath(log_input.map_path)
    config_file = os.path.abspath(log_input.config_file)

    ucpf_fname_list = []
    ucpf_max_num = 10000
    for item in os.listdir(case_path):
        one_case_path = os.path.abspath(os.path.join(case_path, item))
        if not os.path.isdir(one_case_path):
            continue
        valid, ucpf_fname, obj_id = check_junction_case_validity(one_case_path)
        if not valid:
            continue

        cmd = "rm " + one_case_path + "/*feature*"
        os.system(cmd)

        ucpf_fname_list.append(ucpf_fname)
        if len(ucpf_fname_list) >= ucpf_max_num:
            break

    prepare(config_file, ucpf_fname_list)

    cmd = "cp " + config_file + " " + run_path
    os.system(cmd)

    cmd = "cp " + map_path + "/*" + " " + run_path + "/data/"
    os.system(cmd)

if __name__ == "__main__":
    main()
