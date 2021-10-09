import math
import numpy as np
import argparse
import string
import re
import os
import json

DAYS_IN_MONTHS = {1: 31, 3: 31, 5: 31, 7: 31, 8: 31, 10: 31, 12: 31, \
                  4: 30, 6: 30, 9: 30, 11: 30}
SECONDS_IN_DAY = 86400

class pred_scenario_data():
    def __init__(self):
        self.frame_idx = []
        self.obj_id = []
        self.scenario = []
        self.cnt = []
        self.timestamp = []
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

                    line_split = line.split('INFO')
                    data_list = line_split[0].split('.')
                    timestamp = data_list[0].replace(" ", "")
                    timestamp = timestamp.replace(":", "")
                    timestamp = timestamp.replace("-", "")
                    timestamp = "20" + timestamp
                    self.timestamp.append(timestamp)

                line = log.readline()

def get_prev_timestamp(timestamp, cnt):
    data_list = list(timestamp)
    second = (int)(('' if data_list[-2] == '0' else data_list[-2]) + data_list[-1])
    minute = (int)(('' if data_list[-4] == '0' else data_list[-4]) + data_list[-3])
    hour = (int)(('' if data_list[-6] == '0' else data_list[-6]) + data_list[-5])
    day = (int)(('' if data_list[-8] == '0' else data_list[-8]) + data_list[-7])
    month = (int)(('' if data_list[-10] == '0' else data_list[-10]) + data_list[-9])
    year = (int)("".join(data_list[0: 4]))

    curr_second = 60 * minute + second + 3600 * hour
    second_changed = (int)(cnt * 0.1)

    if second_changed <= curr_second:
        second_rem = curr_second - second_changed
        new_hour = (int) (second_rem / 3600)
        new_minute = (int) (np.remainder(second_rem, 3600) / 60)
        new_second = (int) (np.remainder(np.remainder(second_rem, 3600), 60))
        new_day = day
        new_month = month
        new_year = year
    else:
        second_rem = SECONDS_IN_DAY - (second_changed - curr_second)
        new_hour = (int) (second_rem / 3600)
        new_minute = (int) (np.remainder(second_rem, 3600) / 60)
        new_second = (int) (np.remainder(np.remainder(second_rem, 3600), 60))
        new_day = day - 1
        new_month = month
        new_year = year
        if new_day < 0:
            new_month = month - 1
            if new_month < 0:
                new_year = year - 1
                new_month = 12
                new_day = 31
            else:
                if new_month != 2:
                    new_day = DAYS_IN_MONTHS[new_month]
                else:
                    new_day = 29 if np.remainder(year, 4) == 0 else 28

    for i in range(len(data_list)):
        data_list.pop()

    data_list.append(str(new_year))
    data_list.append(str(new_month) if new_month >= 10 else "0" + str(new_month))
    data_list.append(str(new_day) if new_day >= 10 else "0" + str(new_day))
    data_list.append(str(new_hour) if new_hour >= 10 else "0" + str(new_hour))
    data_list.append(str(new_minute) if new_minute >= 10 else "0" + str(new_minute))
    data_list.append(str(new_second) if new_second >= 10 else "0" + str(new_second))

    return "".join(data_list)

def get_future_timestamp(timestamp, cnt):
    data_list = list(timestamp)
    second = (int)(('' if data_list[-2] == '0' else data_list[-2]) + data_list[-1])
    minute = (int)(('' if data_list[-4] == '0' else data_list[-4]) + data_list[-3])
    hour = (int)(('' if data_list[-6] == '0' else data_list[-6]) + data_list[-5])
    day = (int)(('' if data_list[-8] == '0' else data_list[-8]) + data_list[-7])
    month = (int)(('' if data_list[-10] == '0' else data_list[-10]) + data_list[-9])
    year = (int)("".join(data_list[0: 4]))

    curr_second = 60 * minute + second + 3600 * hour
    second_changed = (int)(cnt * 0.1)

    if second_changed + curr_second < SECONDS_IN_DAY:
        second_rem = curr_second + second_changed
        new_hour = (int) (second_rem / 3600)
        new_minute = (int) (np.remainder(second_rem, 3600) / 60)
        new_second = (int) (np.remainder(np.remainder(second_rem, 3600), 60))
        new_day = day
        new_month = month
        new_year = year
    else:
        second_rem = (second_changed + curr_second) - SECONDS_IN_DAY
        new_hour = (int) (second_rem / 3600)
        new_minute = (int) (np.remainder(second_rem, 3600) / 60)
        new_second = (int) (np.remainder(np.remainder(second_rem, 3600), 60))
        new_day = day + 1
        new_month = month
        new_year = year

        if new_month != 2:
            max_day = DAYS_IN_MONTHS[new_month]
            if max_day < new_day:
                new_month = new_month + 1
                new_day = 1
        else:
            max_day = 29 if np.remainder(year, 4) == 0 else 28
            if max_day < new_day:
                new_month = new_month + 1
                new_day = 1
        if new_month > 12:
            new_month = 1
            new_year = new_year + 1

    for i in range(len(data_list)):
        data_list.pop()

    data_list.append(str(new_year))
    data_list.append(str(new_month) if new_month >= 10 else "0" + str(new_month))
    data_list.append(str(new_day) if new_day >= 10 else "0" + str(new_day))
    data_list.append(str(new_hour) if new_hour >= 10 else "0" + str(new_hour))
    data_list.append(str(new_minute) if new_minute >= 10 else "0" + str(new_minute))
    data_list.append(str(new_second) if new_second >= 10 else "0" + str(new_second))

    return "".join(data_list)

def timestamp_comp(ts_1, ts_2):
    list_1 = list(ts_1)
    second_1 = (int)(('' if list_1[-2] == '0' else list_1[-2]) + list_1[-1])
    minute_1 = (int)(('' if list_1[-4] == '0' else list_1[-4]) + list_1[-3])
    hour_1 = (int)(('' if list_1[-6] == '0' else list_1[-6]) + list_1[-5])
    day_1 = (int)(('' if list_1[-8] == '0' else list_1[-8]) + list_1[-7])
    month_1 = (int)(('' if list_1[-10] == '0' else list_1[-10]) + list_1[-9])
    year_1 = (int)("".join(list_1[0: 4]))

    list_2 = list(ts_2)
    second_2 = (int)(('' if list_2[-2] == '0' else list_2[-2]) + list_2[-1])
    minute_2 = (int)(('' if list_2[-4] == '0' else list_2[-4]) + list_2[-3])
    hour_2 = (int)(('' if list_2[-6] == '0' else list_2[-6]) + list_2[-5])
    day_2 = (int)(('' if list_2[-8] == '0' else list_2[-8]) + list_2[-7])
    month_2 = (int)(('' if list_2[-10] == '0' else list_2[-10]) + list_2[-9])
    year_2 = (int)("".join(list_2[0: 4]))

    if year_1 < year_2:
        return True
    elif year_1 > year_2:
        return False

    if month_1 < month_2:
        return True
    elif month_1 > month_2:
        return False

    if day_1 < day_2:
        return True
    elif day_2 > day_1:
        return False

    if hour_1 < hour_2:
        return True
    elif hour_1 > hour_2:
        return False

    if minute_1 < minute_2:
        return True
    elif minute_1 > minute_2:
        return False

    if second_1 <= second_2:
        return True
    else:
        return False

    return False

def build_scenario_case(log_path, ucdf_fname, start_ts, end_ts, run_path, \
                        case_path, scenario, obj_id):
    ucdf_path = os.path.join(log_path, ucdf_fname)
    cmd = "cd " + run_path + " && bin/uos_replay-trunc -f " + \
        ucdf_path + " -s " + start_ts + " -e " + end_ts
    os.system(cmd)

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
    cmd = "cp " + os.path.join(log_path, "uos_local_planner*")  + " " + \
        os.path.join(store_path, "log_files")
    os.system(cmd)

    scenario_case_dir = str(scenario) + "_" + str(obj_id) + "_" + \
        start_ts + "-" + end_ts
    cmd = "cd " + store_path + " && mkdir -p " + scenario_case_dir
    os.system(cmd)

    scenario_case_path = os.path.join(store_path, scenario_case_dir)
    trunc_ucdf_fname = os.path.basename(ucdf_path)
    trunc_ucdf_fname = trunc_ucdf_fname.split(".")[0] + "_" + start_ts + "-" + \
        end_ts + ".ucdf"
    trunc_ucdf_path = os.path.join(run_path, trunc_ucdf_fname)
    cmd = "mv " + trunc_ucdf_path + " " + scenario_case_path
    os.system(cmd)

    case_json_dict = {}
    case_json_dict["scenario"] = scenario
    case_json_dict["obj_id"] = obj_id
    case_json_dict["start_ts"] = start_ts
    case_json_dict["end_ts"] = end_ts
    case_json_dict["start_frame"] = -1
    case_json_dict["end_frame"] = -1
    case_json_fname = os.path.join(scenario_case_path, "case.json")
    file_obj = open(case_json_fname, 'w')
    if file_obj:
        json.dump(case_json_dict, file_obj, sort_keys=True, indent=4)
    else:
        raise ValueError("Failed to write to case.json!")

    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log-path', action='store', dest='log_path', \
                        default="None", help='path containing logs and ucdfs')
    parser.add_argument('--run-path', action='store', dest='run_path', \
                        default="None", help='uos run path')
    parser.add_argument('--case-path', action='store', dest='case_path', \
                        default="None", help='path to store scenario cases')
    parser.add_argument('--scenario', action='store', dest='scenario', \
                        default=-1, help='path to store scenario cases')
    log_input = parser.parse_args()

    if not os.path.exists(log_input.log_path) or not os.path.isdir(log_input.log_path):
        print("Invalid log path!")
        return
    log_path = os.path.normpath(log_input.log_path)

    if not os.path.exists(log_input.run_path) or not os.path.isdir(log_input.run_path):
        print("Invalid run path!")
        return
    run_path = os.path.normpath(log_input.run_path)

    if not os.path.exists(log_input.case_path) or not os.path.isdir(log_input.case_path):
        print("Invalid case path!")
        return
    case_path = os.path.normpath(log_input.case_path)

    start_timestamp = []
    end_timestamp = []
    obj_id = []
    scenario = []
    ucdf = []
    for root, dirs, files in os.walk(log_path, topdown=False):
        for fname in files:
            if fname.find("local_planner") >= 0 and \
               fname.find(".log") >= 0:
                file_path = os.path.join(root, fname)

                data = pred_scenario_data()
                data.parse_log_file(file_path)

                for i in range(len(data.timestamp)):
                    start_timestamp.append(
                        get_prev_timestamp(data.timestamp[i], data.cnt[i] + 20))
                    end_timestamp.append(
                        get_future_timestamp(data.timestamp[i], 20))
                    obj_id.append(data.obj_id[i])
                    scenario.append(data.scenario[i])

            if fname.find("ucdf") >= 0:
                ucdf.append(fname)

    ucdf.sort()
    ucdf_ts = []
    for i in range(len(ucdf)):
        ucdf_ts.append((ucdf[i].split(".")[0]).split("_")[1])
    for i in range(len(obj_id)):
        if int(log_input.scenario) != -1:
            if scenario[i] != int(log_input.scenario):
                continue

        print(scenario[i], obj_id[i], start_timestamp[i], end_timestamp[i])
        for j in range(len(ucdf)):
            if timestamp_comp(ucdf_ts[j], start_timestamp[i]):
                if j == len(ucdf) - 1:
                    print("trunc ucdf: ", ucdf[j])
                    build_scenario_case(log_path, ucdf[j], start_timestamp[i], \
                                        end_timestamp[i], run_path, case_path,
                                        scenario[i], obj_id[i])
                    break
                else:
                    continue
            else:
                if j > 0:
                    print("trunc ucdf: ", ucdf[j-1])
                    build_scenario_case(log_path, ucdf[j-1], start_timestamp[i], \
                                        end_timestamp[i], run_path, case_path,
                                        scenario[i], obj_id[i])
                    break
                else:
                    print("No suitable ucdf found to be trunc.")

if __name__ == '__main__':
    main()
