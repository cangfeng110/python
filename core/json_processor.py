import os
import sys
import json
import argparse
import re

COMMENT_SINGLELINE = "//"
COMMENT_MULTILINE_START = "/*"
COMMENT_MULTILINE_END = "*/"
QUOTATION = '"'

def del_key_val_in_dict(dict_, key):
    if not isinstance(dict_, dict):
        return

    for exist_key in dict_.keys():
        if exist_key == key:
            del dict_[key]
            return
        elif isinstance(dict_[exist_key], dict):
            del_key_val_in_dict(dict_[exist_key], key)

    return

def find_key_val_in_dict(dict_, key):
    if not isinstance(dict_, dict):
        raise ValueError("Invalid input dict!")

    found = False
    val = ""

    for exist_key in dict_.keys():
        if exist_key == key:
            return True, dict_[key]
        elif isinstance(dict_[exist_key], dict):
            found, val = find_key_val_in_dict(dict_[exist_key], key)

        if found:
            return found, val

    return found, val

def insert_nested_values_to_dict(dict_, keys, val):
    if not isinstance(dict_, dict):
        print("Not a dict")
        return
    if isinstance(keys, list):
        if len(keys) < 1:
            print("Empty keys!")
            return
        elif len(keys) < 2:
            dict_[keys] = val
            return
    if isinstance(keys, str):
        dict_[keys] = val
        return

    sub_dict = []
    sub_dict.append(dict_)
    for i in range(1, len(keys)):
        if keys[i-1] not in sub_dict[i-1].keys():
            sub_dict[i-1][keys[i-1]] = {}
            sub_dict[i-1][keys[i-1]][keys[i]] = ""
        elif not isinstance(sub_dict[i-1][keys[i-1]], dict):
            sub_dict[i-1][keys[i-1]] = {}
            sub_dict[i-1][keys[i-1]][keys[i]] = ""
        elif keys[i] not in sub_dict[i-1][keys[i-1]].keys():
            sub_dict[i-1][keys[i-1]][keys[i]] = {}
        sub_dict.append(sub_dict[i-1][keys[i-1]])

    sub_dict[-1][keys[-1]] = val

    return

class json_processor:

    def __init__(self, json_file):
        self.file = json_file
        self.success = False

    def remove_single_comments(self, line):
        slash_pos = -1
        pos_base = 0
        while True:
            slash_pos = line.find(COMMENT_SINGLELINE, pos_base)
            if slash_pos == -1:
                return line
            pos_base +=  slash_pos + len(COMMENT_SINGLELINE)
            if line.count(QUOTATION, 0, pos_base) % 2 == 0:
                return line[0:slash_pos]

    def update_line(self, lines, line_num, new_line):
        lines[line_num - 1] = new_line + '\n'

    def read_file(self):
        try:
            jsonSrc = open(self.file, 'r')
        except:
            print('Exception: cannot open ' + self.file)
            return False, ""

        try:
            lines = jsonSrc.read().splitlines()
        except:
            print('Exception: cannot read ' + self.file)
            return False, ""

        return True, lines

    # Remove all comments
    def clear_comments(self, json_lines):
        lines = json_lines
        current_line = 0;
        multi_comment_start = False
        for line in lines:

            current_line += 1

            if len(line) == 0:
                self.update_line(lines, current_line, "")
                continue

            # Remove comments start with '//'
            line = self.remove_single_comments(line)
            if len(line) == 0:
                self.update_line(lines, current_line, "")
                continue

            pos_multi_comment_start = line.find(COMMENT_MULTILINE_START)
            pos_multi_comment_end = line.find(COMMENT_MULTILINE_END)
            if pos_multi_comment_start != -1 and pos_multi_comment_end != -1:
                if multi_comment_start is True:
                    print("Has nesting multi comment.")
                else:
                    tmp_pos_multi_comment_start = \
                        line.find(COMMENT_MULTILINE_START, pos_multi_comment_start+len(COMMENT_MULTILINE_START))
                    if tmp_pos_multi_comment_start != -1:
                        tmp_pos_multi_comment_end = \
                            line.find(COMMENT_MULTILINE_END, tmp_pos_multi_comment_start)
                        if tmp_pos_multi_comment_end != -1:
                            print("Has nesting multi comment.")

                line = line.replace(line[pos_multi_comment_start: \
                        pos_multi_comment_end + \
                        len(COMMENT_MULTILINE_END)], "")
            elif pos_multi_comment_start != -1:
                line = line[0:pos_multi_comment_start]
                if multi_comment_start is True:
                    print("Has nesting multi comment.")
                else:
                    multi_comment_start = True
            elif pos_multi_comment_end != -1:
                line = line[pos_multi_comment_end + \
                        len(COMMENT_MULTILINE_END):]
                multi_comment_start = False
            elif multi_comment_start == True:
                self.update_line(lines, current_line, "")
                continue
            if len(line) == 0:
                self.update_line(lines, current_line, "")
                continue

            self.update_line(lines, current_line, line)

        # Generate json string and send to python.json
        json_string = ""
        for line in lines:
            json_string += line

        return json_string

    def read_json_as_dict(self):
        res, lines = self.read_file()
        if False == res:
            return False

        return json.loads(self.clear_comments(lines))

    def write_dict_to_json(self, json_dict):
        output_fname = os.path.dirname(os.path.normpath(self.file))
        output_fname = os.path.join(output_fname, os.path.basename(self.file))
        file_obj = open(output_fname, 'w')

        if file_obj:
            json.dump(json_dict, file_obj, sort_keys=True, indent=4)
        else:
            raise ValueError("Failed to write to uos_common.json!")

    def clear_json_comments(self):
        json_dict = self.read_json_as_dict()
        self.write_dict_to_json(json_dict)
        return

    def del_key_val_in_json(self, key):
        json_dict = self.read_json_as_dict()
        del_key_val_in_dict(json_dict, key)
        self.write_dict_to_json(json_dict)
        return

    def find_key_val_in_json(self, key):
        json_dict = self.read_json_as_dict()
        return find_key_val_in_dict(json_dict, key)

    def insert_key_val_to_json(self, keys, val):
        json_dict = self.read_json_as_dict()
        insert_nested_values_to_dict(json_dict, keys, val)
        self.write_dict_to_json(json_dict)
        return
