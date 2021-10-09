import json
import os
import math
import numpy as np
import argparse
import string
import pandas as pd
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.models import BayesianModel

epsilon = 0.001

def parser_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', action='store', dest='config_json', \
                        default="/tmp/config.json", help='config.json')

    parser.add_argument('--feature-annotation', action='store', \
                        dest='feature_annotation', default="None", \
                        help='file containing features and annotations')

    parser.add_argument('--output-fname', action='store', dest='output_fname', \
                        default="/tmp/cpd.xlsx", \
                        help='file name path for saving the resulting cpds')

    parser.add_argument('--prior-path', action='store', dest='prior_path', \
                        default="/tmp/", \
                        help='path for saving the prior cpds')

    global log_input
    log_input = parser.parse_args()

def read_feature_annotation(file_path):
    if not os.path.exists(file_path):
        raise ValueError("feature_annotation file not exists!")

    data = pd.read_pickle(file_path)
    data["class_label"] = data["class_label"].astype(int)

    return data

def get_feature_discre_val(orig_val, discre_list):
    for i in range(len(discre_list) - 1):
        if (orig_val >= discre_list[i]) & (orig_val < discre_list[i+1]):
            return i

    return len(discre_list) - 1

def feature_discretization(data, config_dict):
    n_samples = data.shape[0]
    for feature in config_dict['feature_name']:
        for j in range(n_samples):
            discre = config_dict['feature_discre'][feature]

            missing_val = data[feature].isnull()

            if missing_val.iloc[j]:
                data[feature].iat[j] = np.NaN
            else:
                data[feature].iat[j] = \
                    get_feature_discre_val(data[feature].iat[j], discre)

    return data

class posterior_cpd():
    def __init__(self, num_samples):
        self.n_samples = num_samples
        self.variables = []
        self.cpds = {}

    def add_cpd(self, variable, cpd_arr):
        self.variables.append(variable)
        if variable in self.cpds.keys():
            print("This {variable} is already in cpds!".format(variable=variable))
        else:
            self.cpds[variable] = cpd_arr

    def to_json_dict(self):
        ret_dict = dict(prior_sample_size=self.n_samples, prior_cpds=self.cpds)
        return ret_dict

    def dump_to_json_file(self, file_path):
        file_obj = open(file_path, 'w')
        if file_obj:
            json.dump(self.to_json_dict(), file_obj)
        else:
            raise ValueError("Cannot open file!\n")

def main():
    parser_options()
    if os.path.exists(log_input.config_json):
        config_object = open(log_input.config_json, 'r')
        config_dict = json.load(config_object)
    else:
        raise ValueError("Invalid config json!")

    feature_annotation = \
        read_feature_annotation(log_input.feature_annotation)

    feature_discretization(feature_annotation, config_dict)
    n_samples = feature_annotation.shape[0]

    model = BayesianModel()
    for i in range(config_dict['n_features']):
        model.add_edge('class_label', config_dict['feature_name'][i])

    model.fit(feature_annotation, estimator=MaximumLikelihoodEstimator)

    writer = pd.ExcelWriter(os.path.abspath(log_input.output_fname), \
                            engine='xlsxwriter')
    workbook = writer.book
    worksheet = workbook.add_worksheet('cpd')
    writer.sheets['cpd'] = worksheet

    # read prior json
    prior_json = os.path.join(log_input.prior_path, "prior.json")
    prior_json_found = False
    prior_dict = {}
    n_samples_prior = 0
    if os.path.exists(prior_json):
        prior_json_found = True
        prior_json_object = open(prior_json, 'r')
        prior_dict = json.load(prior_json_object)
        n_samples_prior = prior_dict['prior_sample_size']

    post_cpds = posterior_cpd(n_samples + n_samples_prior)

    # get cpds
    curr_row = 0
    for feature in config_dict['feature_name']:
        for cpd in model.get_cpds():
            if cpd.variable != feature:
                continue
            print("Computing cpd of {var}...".format(var=feature))

            feature_discre = config_dict['feature_discre'][feature]
            n_interval = len(feature_discre)
            cpd_arr = np.zeros([n_interval, 4], dtype=object)

            # get interval string
            for i in range(n_interval - 1):
                cpd_arr[i, 0] = "[" +  str(format(feature_discre[i], '.2f')) + \
                    ", " + str(format(feature_discre[i+1], '.2f')) + "]"
            cpd_arr[n_interval - 1, 0] = "[" + \
                str(format(feature_discre[-1], '.2f')) + ", inf]"

            # get values from the learnt cpd
            indices = cpd.state_names[feature]
            val = cpd.get_values()
            sum = epsilon * n_interval
            for i in range(len(indices)):
                cpd_arr[int(indices[i]), 1] = val[i]
                sum = sum + val[i]
            cpd_arr[:, 1] = (cpd_arr[:, 1] + epsilon) / sum

            # get prior cpd and sample size
            if prior_json_found:
                prior_cpd_arr = prior_dict['prior_cpds'][feature]
                prior_cpd_arr = np.array(prior_cpd_arr)
                if prior_cpd_arr.shape[0] != n_interval:
                    raise ValueError("The prior cpd is not in the right shape!\n")
                cpd_arr[:, 2] = prior_cpd_arr

            # compute the resulting cpd using Bayesian estimation method.
            cpd_arr[:, 3] = (cpd_arr[:, 1] * n_samples + cpd_arr[:, 2] * n_samples_prior) / \
                (n_samples + n_samples_prior)

            print("Done.")

            post_cpds.add_cpd(feature, np.array(cpd_arr[:, 3], dtype=float).tolist())

            # assemble dataframe and write results to file
            df = pd.DataFrame(cpd_arr, columns=['interval', 'MLE', 'prior', 'res'])
            df.name = feature
            df['MLE'] = df['MLE'].astype(float)
            df['prior'] = df['prior'].astype(float)
            df['res'] = df['res'].astype(float)

            worksheet.write_string(curr_row, 0, df.name)
            for i in range(1, df.shape[1]):
                worksheet.write_string(curr_row, i, df.columns[i])
            df.to_excel(writer, sheet_name='cpd', startrow=curr_row+1, startcol=0,\
                        header=None, index=None)

            curr_row = curr_row + 1 + df.shape[0] + 1

            post_cpds.dump_to_json_file(os.path.join(log_input.prior_path, "prior_new.json"))

    writer.save()
if __name__ == '__main__':
    main()
