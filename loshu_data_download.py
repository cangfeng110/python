import argparse
import string
import re
import os
import json
from datetime import datetime

MIN_FILE_SIZE = 1024 * 1024

class search_result_data():
    def __init__(self):
        self.log_paths = []
        self.names = []
        self.size = []
        return

    def parse_log_file(self, log_file):
        path_pattern = re.compile(r'.*path')
        size_pattern = re.compile(r'.*size')
        name_pattern = re.compile(r'.*\'name')
        with open(log_file, 'r') as log:
            line = log.readline()

            while line:
                line = line.rstrip(',\n')
                match = path_pattern.match(line)
                if match:
                    line_split = line.split('path\': ')
                    self.log_paths.append(line_split[1])

                match = size_pattern.match(line)
                if match:
                    line_split = line.split('size\': ')
                    self.size.append(int(line_split[1]))

                match = name_pattern.match(line)
                if match:
                    line_split = line.split('name\': ')
                    self.names.append(line_split[1])

                line = log.readline()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdate', action='store', dest='start_date', default="None")
    parser.add_argument("--edate", action="store", dest="end_date", default="None")
    parser.add_argument("--vehicle-name", action="store", dest="vehicle_name", default="None")
    parser.add_argument('--output-path', action='store', dest='output_path', \
                        default="None", help='uos run path')
    log_input = parser.parse_args()

    start_date = log_input.start_date
    end_date = log_input.end_date
    if start_date != datetime.strptime(start_date, "%Y-%m-%d").strftime('%Y-%m-%d'):
        raise ValueError("Invalid start_date format!")
    if end_date != datetime.strptime(end_date, "%Y-%m-%d").strftime('%Y-%m-%d'):
        raise ValueError("Invalid end_date format!")

    if not os.path.exists(log_input.output_path) or not \
       os.path.isdir(log_input.output_path):
        print("Invalid output path!")
        return
    output_path = os.path.normpath(log_input.output_path)

    start_time_str = start_date + ' 00:00:00'
    end_time_str = end_date + ' 00:00:00'

    cmd = "./loshu-client -u 'zs10438' -p 'Zs271828;' -m search --start_time '" + \
        start_time_str + "' --end_time '" + end_time_str + \
        "' --vehicle_name " + log_input.vehicle_name + " --name " + \
        log_input.vehicle_name + "_log" + " > search.txt"
    os.system(cmd)

    data = search_result_data()
    data.parse_log_file("search.txt")

    for i in range(len(data.size)):
        if data.size[i] < MIN_FILE_SIZE:
            continue
        fname = data.names[i].rstrip("'").lstrip("'")
        fname = os.path.join(output_path, fname)
        print("Downloading " + fname)

        cmd = "./loshu-client -u 'zs10438' -p 'Zs271828;' -m download " + \
            " --key " + data.log_paths[i] + " --output " + fname
        os.system(cmd)

        cmd = "tar zxf " + fname + " -C" + output_path
        os.system(cmd)
        cmd = "rm " + fname
        os.system(cmd)

    cmd = "rm search.txt"
    os.system(cmd)

if __name__ == '__main__':
    main()
