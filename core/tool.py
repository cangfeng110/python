#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 09:53:20 2019

@author: uisee
"""
import os
import math
import shutil
import re
import xlrd
import xlwt
from xlutils.copy import copy

# caution: the API could delete some important files by mistake
def del_file(path):
    warning_str = input("delete folder %s? (yes/no): " % path)
    if warning_str != 'yes':
        return
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            shutil.rmtree(c_path,True)
        else:
            os.remove(c_path)

def del_file_with_type(path, file_type):
    ls = os.listdir(path)
    for i in ls:
        data = i.split('/')
        if data[-1].endswith(file_type) is False:
            continue
        c_path = os.path.join(path, i)
        os.remove(c_path)

def dot_2d(v1, v2):
    return v1.x * v2.x + v1.y * v2.y

def calc_projection_scale(axis, polygon):
    d = dot_2d(axis, polygon.vertexes[0])
    min_d = d
    max_d = d
    for i in range(1,len(polygon.vertexes)):
        d = dot_2d(axis, polygon.vertexes[i])
        if d < min_d:
            min_d = d
        elif d > max_d:
            max_d = d
    return min_d, max_d

def is_axis_seperate_polygons(axis, polygon_a, polygon_b):
    mina, maxa = calc_projection_scale(axis, polygon_a)
    minb, maxb = calc_projection_scale(axis, polygon_b)
    if maxa < minb or maxb < mina:
        return True
    else:
        return False

def collision_detection_two_polygons(polygon_a, polygon_b):
    distance_a_2_b = math.sqrt((polygon_a.center_pt.x - polygon_b.center_pt.x) ** 2 + \
                               (polygon_a.center_pt.y - polygon_b.center_pt.y) ** 2)
    if distance_a_2_b > polygon_a.radius + polygon_b.radius:
        return False
    for axis in polygon_a.axises:
        if is_axis_seperate_polygons(axis, polygon_a, polygon_b):
            return False

    for axis in polygon_b.axises:
        if is_axis_seperate_polygons(axis, polygon_a, polygon_b):
            return False
    return True

def trans_one_pos_to_local(o_x, o_y, o_theta, g_x, g_y):
    dx = g_x - o_x
    dy = g_y - o_y
    #o_theta = math.pi / 2.0 - o_theta
    return math.cos(o_theta) * dx - math.sin(o_theta) *dy,\
            math.sin(o_theta) * dx + math.cos(o_theta) *dy

def calc_dist(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx ** 2 + dy **2)

def listdir(path, list_name): #传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            list_name.append(file_path)

def newestfile(target_list):
    pattern = re.compile(r'.*log_.*')
    newest_time = os.path.getmtime(target_list[0])
    index = 0
    for i in range(len(target_list)):
        tmp_time = os.path.getmtime(target_list[i])
        if newest_time <= tmp_time and pattern.match(target_list[i]):
            newest_time = tmp_time
            index = i
    return target_list[index]

def write_excel_xls_append(path, value):
    if os.path.exists(path) is False:
        workbook = xlwt.Workbook()
        workbook.add_sheet(u'Sheet1')
        workbook.save(path)

    index = len(value)
    workbook = xlrd.open_workbook(path)
    sheets = workbook.sheet_names()
    worksheet = workbook.sheet_by_name(sheets[0])
    rows_old = worksheet.nrows
    new_workbook = copy(workbook)
    new_worksheet = new_workbook.get_sheet(0)
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i+rows_old, j, value[i][j])
    new_workbook.save(path)

def get_average_value(data, use_fabs=False):
    data_size = len(data)
    if data_size <= 0:
        print("Warning: data size error!")
        return 0.0

    ave_value = 0.0
    for value in data:
        if use_fabs:
            ave_value += math.fabs(value)
        else:
            ave_value += value

    return ave_value / len(data)

def get_pos_dist(x_set1, y_set1, x_set2, y_set2):
    res = list(map(lambda x:math.sqrt((x[0] - x[2])**2 + (x[1] - x[3])**2),
               zip(x_set1, y_set1, x_set2, y_set2)))
    return res

def trans_one_pos_to_local(o_x, o_y, o_theta, g_x, g_y):
    dx = g_x - o_x
    dy = g_y - o_y
    o_theta = math.pi / 2.0 - o_theta
    return math.cos(o_theta) * dx - math.sin(o_theta) *dy,\
            math.sin(o_theta) * dx + math.cos(o_theta) *dy

def trans_pos_to_local(ori_x_set, ori_y_set, ori_theta_set,
                       glo_x_set, glo_y_set):
    local_x = []
    local_y = []
    for i in range(len(ori_x_set)):
        x, y = trans_one_pos_to_local(ori_x_set[i], ori_y_set[i],
                                      ori_theta_set[i], glo_x_set[i],
                                      glo_y_set[i])
        local_x.append(x)
        local_y.append(y)
    return local_x, local_y

def accumulate_data_2d(data, data_2d, use_fabs=False):
    for i in range(min(len(data), len(data_2d[0]))):
        data_2d[1][i] += 1
        if use_fabs:
            data_2d[0][i] += math.fabs(data[i])
        else:
            data_2d[0][i] += data[i]
    return data_2d

def get_average_data_2d(data_2d):
    data = data_2d[0]
    count = data_2d[1]
    count_sum = 0
    value_sum = 0.0
    for i in range(len(count)):
        count_sum += count[i]
        value_sum += data[i]
    return value_sum / max(count_sum, 1)

def get_average_data_2d_seperate(data_2d):
    tmp_val = []
    for i in range(len(data_2d[0])):
        if 0 != data_2d[1][i]:
            tmp_res = data_2d[0][i] / data_2d[1][i]
            tmp_val.append(tmp_res)
        else:
            break
    return tmp_val
