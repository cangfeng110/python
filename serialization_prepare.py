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

def prepare(json_file, ucdf_name, map_path, run_path):
    processor = json_processor.json_processor(json_file)
    for redundant_key in redundant_mod_keys:
        processor.del_key_val_in_json(redundant_key)

    processor.insert_key_val_to_json(["_MOD_uos_config", "run_scene"], "replay")
    processor.insert_key_val_to_json(["_MOD_uos_config", "platform"], "SMP")
    processor.insert_key_val_to_json(["_MOD_uos_config", "replay_fname"], \
                                     "data/" + ucdf_name)
    processor.insert_key_val_to_json(["_MOD_uos_local_planner", "dump_ucpf"], 1)
    processor.insert_key_val_to_json(["_MOD_uos_local_planner", \
                                      "ucpf_dump_fname"], "data/test.ucpf")
    processor.insert_key_val_to_json(["_MOD_uos_local_planner", \
                                      "prediction_replay"], 0)
    processor.del_key_val_in_json("st_decision")

    roadmap_fname = processor.find_key_val_in_json('roadmap_fname')[1]
    if roadmap_fname != "":
        roadmap = roadmap_fname.split('/')[-1]
        processor.insert_key_val_to_json(["_MOD_uos_config", "roadmap_fname"], \
                                         "data/" + roadmap)

        map_found = False
        for root, dirs, files in os.walk(map_path, topdown=False):
            for fname in files:
                if fname.find(".hmap") != -1 or fname.find(".rmap") != -1:
                    map_fname = os.path.normpath(os.path.join(root, fname))
                    cmd = "cp " + map_fname + " " + run_path + "/data/"
                    os.system(cmd)
                    map_found = True
                    print("Successfully copied {} to run path.".format(map_fname))
        if not map_found:
            raise ValueError("map file not found!")

    else:
        raise ValueError("roadmap is not found in uos_common.json!")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-path", action="store", dest="case_path", default="None")
    parser.add_argument('--run-path', action='store', dest='run_path', default="None")
    parser.add_argument('--map-path', action='store', dest='map_path', default="None")
    parser.add_argument('--config-path', action='store', dest='config_path', default="None")
    parser.add_argument("--ucdf-name", action="store", dest="ucdf_name", default="None")
    log_input = parser.parse_args()

    if not os.path.exists(log_input.case_path):
        raise ValueError("Invalid case path!")
    if not os.path.exists(log_input.run_path):
        raise ValueError("Invalid run path!")
    if not os.path.exists(log_input.map_path):
        raise ValueError("Invalid map path!")
    if not os.path.exists(log_input.config_path):
        raise ValueError("Invalid config path!")
    if log_input.ucdf_name == "":
        raise ValueError("Invalid ucdf name!")

    run_path = os.path.abspath(log_input.run_path)
    case_path = os.path.abspath(log_input.case_path)
    map_path = os.path.abspath(log_input.map_path)
    config_path = os.path.abspath(log_input.config_path)
    ucdf_name = log_input.ucdf_name

    ucdf_found = False
    for fname in os.listdir(case_path):
        if fname != ucdf_name:
            continue
        ucdf_fname = os.path.abspath(os.path.join(case_path, fname))
        cmd = "cp " + ucdf_fname + " " + run_path + "/data/"
        os.system(cmd)
        ucdf_found = True
        break
    if not ucdf_found:
        raise ValueError("ucdf file not found!")

    print("Start processing {}...".format(ucdf_name))

    common_json_found = False
    for fname in os.listdir(config_path):
        if fname != "uos_common.json":
            continue
        json_fname = os.path.abspath(os.path.join(config_path, fname))
        prepare(json_fname, ucdf_name, map_path, run_path)
        cmd = "cp " + json_fname + " " + run_path
        os.system(cmd)
        common_json_found = True
        break
    if not common_json_found:
        raise ValueError("common json file not found!")

if __name__ == "__main__":
    main()
