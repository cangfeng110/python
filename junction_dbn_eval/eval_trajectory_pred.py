import os
import sys
import math
import copy
import json
import numpy as np
import argparse
import string
import re
sys.path.append('..')
import core.trajectoryParser as traj_parser
import core.tool as mytool
from decimal import Decimal
import pandas as pd
import pickle

PRED_EVAL_TIME      = 3.0
PREDICTION_INTERVAL = 0.3

class traj_evaluator():
    def __init__(self, local_planner_log, planner_log):
        parseLogFile = traj_parser.ParseLogFile(local_planner_log, planner_log)
        self.true_traj, self.pred_trajSet_set, self.ucdf_idxes, self.ucdf_ts = \
                parseLogFile.parse_data()

    def get_traj_data(self, traj):
        base_pos = self.true_traj.pos_set[0]
        traj_x = []
        traj_y = []
        for pos in traj.pos_set:
            traj_x.append(pos.x - base_pos.x)
            traj_y.append(pos.y - base_pos.y)

        return traj_x, traj_y

    def get_need_eval_ucdf_indexes(self):
        true_x, true_y = self.get_traj_data(self.true_traj)

        idxes = [0]
        for i in range(1, len(true_x)):
            if abs(true_x[i-1] - true_x[i]) > 1e-5 or \
               abs(true_y[i-1] - true_y[i]) > 1e-5:
                idxes.append(i)
        # TODO:handle no pred traj situation
        return idxes

    def get_true_traj_data_without_redundant(self):
        idxes = self.get_need_eval_ucdf_indexes()
        tmp_x, tmp_y = self.get_traj_data(self.true_traj)
        true_x = []
        true_y = []
        for idx in idxes:
            true_x.append(tmp_x[idx])
            true_y.append(tmp_y[idx])
        return true_x, true_y

    def get_ucdf_ts_without_redundant(self):
        idxes = self.get_need_eval_ucdf_indexes()

        ucdf_ts = []
        for idx in idxes:
            ucdf_ts.append(self.ucdf_ts[idx] - self.ucdf_ts[0])

        return ucdf_ts

    def rm_redundant_pred_trajSet(self):
        idxes = self.get_need_eval_ucdf_indexes()

        trajSet_set = []
        for idx in idxes:
            trajSet_set.append(self.pred_trajSet_set.trajSet_set[idx])
        return trajSet_set

    def aligning_trajs(self, i, pred_x, pred_y, true_x, true_y, true_ts):
        # aligned true traj
        x_set1 = []
        y_set1 = []
        # aligned pred traj
        x_set2 = []
        y_set2 = []
        ts_base_i = []
        for j in range(i, len(true_x)):
            ts_base_i.append(true_ts[j] - true_ts[i])
        if len(ts_base_i) < 2:
            return x_set1, y_set1, x_set2, y_set2

        index = 0
        for j in range(len(pred_x)):
            time_min_dist = sys.float_info.max
            elapse_time = j * PREDICTION_INTERVAL
            for k in range(index, len(ts_base_i)):
                tmp = math.fabs(elapse_time - ts_base_i[k])
                if tmp < time_min_dist:
                    time_min_dist = tmp
                    index = k

            if (len(ts_base_i) - 1) == index and \
                    elapse_time > ts_base_i[index]:
                continue

            x_set2.append(pred_x[j])
            y_set2.append(pred_y[j])

            if math.fabs(elapse_time - ts_base_i[index]) < 1e-3:
                x = true_x[index+i]
                y = true_y[index+i]
                x_set1.append(x)
                y_set1.append(y)
            elif elapse_time - ts_base_i[index] > 0:
                x = true_x[index+i] + (true_x[index+i+1] - true_x[index+i]) * \
                    (elapse_time - ts_base_i[index]) / (ts_base_i[index+1] - ts_base_i[index])
                y = true_y[index+i] + (true_y[index+i+1] - true_y[index+i]) * \
                    (elapse_time - ts_base_i[index]) / (ts_base_i[index+1] - ts_base_i[index])
                x_set1.append(x)
                y_set1.append(y)
            else:
                x = true_x[index+i-1] + (true_x[index+i] - true_x[index+i-1]) * \
                    (elapse_time - ts_base_i[index-1]) / (ts_base_i[index] - ts_base_i[index-1])
                y = true_y[index+i-1] + (true_y[index+i] - true_y[index+i-1]) * \
                    (elapse_time - ts_base_i[index-1]) / (ts_base_i[index] - ts_base_i[index-1])
                x_set1.append(x)
                y_set1.append(y)

        return x_set1, y_set1, x_set2, y_set2

    def get_eval_traj_result_one_frame(self, i, true_x, true_y, ucdf_ts,
                                       eval_point_size, pred_trajSet_set):
        pred_traj_set = pred_trajSet_set[i].traj_set
        pos_err = [sys.float_info.max]

        for pred_traj in pred_traj_set:
            pred_x, pred_y = self.get_traj_data(pred_traj)
            aligned_true_x, aligned_true_y, aligned_pred_x, aligned_pred_y = \
                    self.aligning_trajs(i, pred_x, pred_y, true_x, true_y, ucdf_ts)
            tmp_err = mytool.get_pos_dist(aligned_true_x[0:eval_point_size],
                                          aligned_true_y[0:eval_point_size],
                                          aligned_pred_x[0:eval_point_size],
                                          aligned_pred_y[0:eval_point_size])

            if sum(tmp_err) < sum(pos_err):
                pos_err = tmp_err

        return pos_err

    def get_eval_traj_result(self):
        true_x, true_y = self.get_true_traj_data_without_redundant()
        pred_trajSet_set = self.rm_redundant_pred_trajSet()
        ucdf_ts = self.get_ucdf_ts_without_redundant()

        eval_point_size = math.floor(PRED_EVAL_TIME / PREDICTION_INTERVAL) + 1
        pos_time_err = [ [0.0] * eval_point_size for i in range(2)]
        for i in range(len(true_x)):
            pos_err = self.get_eval_traj_result_one_frame(i, true_x, true_y,
                                                          ucdf_ts, eval_point_size,
                                                          pred_trajSet_set)

            pos_time_err = mytool.accumulate_data_2d(pos_err, pos_time_err, True)

        ave_pos_err = mytool.get_average_data_2d(pos_time_err)
        pos_time_ave_err = mytool.get_average_data_2d_seperate(pos_time_err)

        if len(pos_time_ave_err) == 0:
            print("Warning: No eval datas!")
            end_ave_pos_err = 0.0
        else:
            end_ave_pos_err = pos_time_ave_err[-1]

        return ave_pos_err, end_ave_pos_err

def main():
    # eval traj pred result
    traj_parser.parser_options()
    evaluator = traj_evaluator(traj_parser.log_input.log_file1,
                               traj_parser.log_input.log_file2)
    ave_pos_err, end_ave_pos_err = evaluator.get_eval_traj_result()

    print("ave_pos_err: %.2f" % (ave_pos_err))
    print("end_ave_pos_err: %.2f" % (end_ave_pos_err))

    res_df = pd.DataFrame(columns=["ave_pos_err", "end_ave_pos_err"])
    res_df.loc[-1] = [ave_pos_err, end_ave_pos_err]
    res_df.to_pickle(os.path.join(traj_parser.log_input.case_path, "traj_eval_res.bin"))

if __name__ == '__main__':
    main()
