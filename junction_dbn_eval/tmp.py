import os
import sys
import json
import argparse
import re
import pandas as pd
import pickle
import matplotlib.pyplot as plt

def main():

    traj_res_df = pd.read_excel("/home/haoquan/junction_traj_eval_res_new_dbn_naive_poly.xlsx", \
                            index_col=0)
    dbn_res_df = pd.read_excel("/home/haoquan/junction_dbn_eval_res_new_dbn_naive_poly.xlsx", \
                            index_col=0)

    traj_res_df["mean_brier_score"] = -1.0
    for i in range(traj_res_df.shape[0]):
        traj_case_path = traj_res_df["case_path"].iloc[i]
        ret = dbn_res_df[dbn_res_df["case_path"] == traj_case_path]
        if not ret.empty:
            brier_score = ret["mean_brier_score"].iloc[0]
            traj_res_df["mean_brier_score"].iloc[i] = brier_score

    output_path = "/tmp/junction_eval_res_comp_new_dbn_naive_poly.xlsx"
    traj_res_df.to_excel(output_path)

    num = 0
    for i in range(traj_res_df.shape[0]):
        diff_1 = traj_res_df["ave_pos_err"].iloc[i] - \
            traj_res_df["brd_ave_pos_err"].iloc[i]
        diff_2 = traj_res_df["end_ave_pos_err"].iloc[i] - \
            traj_res_df["brd_end_ave_pos_err"].iloc[i]
        if diff_1 > 1.5 or diff_2 > 1.5:
            print(traj_res_df["case_path"].iloc[i])
            print("ave {:.3f} end {:.3f}".format(diff_1, diff_2))
            plt.scatter(diff_1, diff_2, edgecolors='r', c='None')
        else:
            plt.scatter(diff_1, diff_2, edgecolors='b', c='None')
        if diff_1 < 0.0 and diff_2 < 0.0:
            num += 1

    plt.grid(axis='both')
    plt.xlabel("ave_pos_err_diff")
    plt.ylabel("end_ave_pos_err_diff")
    plt.show()
    print(num)

if __name__ == "__main__":
    main()
