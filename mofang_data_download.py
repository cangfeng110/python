import requests
import argparse
import re
import os
from datetime import datetime

SUCCESS_CODE = 200000000
MIN_FILE_SIZE = 1024 * 1024

class DownLoad:
    def __init__(self, start_date, end_date, vehicle_name, \
                 outDir, parent_id, \
                 host="mofang.uisee.ai", username="zs10438", \
                 password="Zs271828;"):
        self.host = host
        self.outDir = outDir
        self.parent_id = parent_id
        self.username = username
        self.password = password
        self.start_date = start_date
        self.end_date = end_date
        self.vehicle_name = vehicle_name

    def getFiles(self, host,parentId,cookies):
        url = 'http://{}/api/files/listdir_all_files'.format(host)
        response = requests.get(url, params={'parent': parentId},
                                cookies=cookies)
        return response.json()['files']

    def getAllFiles(self, host,parentId,cookies):
        url = 'http://{}/api/files/listdir_all_files'.format(host)
        response = requests.get(url, params={'parent': parentId},
                                cookies=cookies)

        res = []
        file_list = response.json()['files']
        for file in file_list:
            if file['type'] == 'D':
                res.extend(self.getAllFiles(host, file['id'], cookies))
            else:
                res.append(file)

        return res

    def downloadFile(self, host,file,cookies,dirpath):
        url = 'http://{}/api/files/{}/download'.format(host, file['id'])
        abspath = os.path.join(dirpath, file['name'])
        response = requests.get(url, cookies=cookies, allow_redirects=False)

        if 'location' in response.headers:
            url = response.headers['location']
        else:
            print('[FAILED] download {} error, fail to register download'.format(
                abspath))
            return False

        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(abspath, 'wb') as f:
                f.write(response.raw.read())

        print("Downloaded successfully.")

        return True

    def mainLoop(self):
        ret = False
        if not os.path.exists(self.outDir):
            raise ValueError("Outdir does not exist!")

        loginUrl = 'http://{}/api/security/login'.format(self.host)
        cookies = {}
        response = requests.post(loginUrl, data={
            'username': self.username,
            'password': self.password
        })
        if response.json()['code'] == SUCCESS_CODE:
            cookies['sessionid'] = response.cookies['sessionid']
        else:
            print('login failed')
            return False

        name_pattern = self.vehicle_name + "_log"
        logList = self.getAllFiles(self.host,self.parent_id,cookies)
        for log in logList:
            if log['created'] >= self.start_date and \
               log['created'] < self.end_date and \
               log['name'].find(name_pattern) >= 0 and \
               log['size'] >= MIN_FILE_SIZE:
                print("Downloading {}...".format(log['name']))
                ret = self.downloadFile(self.host,log,cookies,self.outDir)
                if ret:
                    log_fname = os.path.join(self.outDir, log['name'])
                    cmd = "tar zxf " + log_fname + " -C" + self.outDir
                    os.system(cmd)
                    cmd = "rm " + log_fname
                    os.system(cmd)

        logoutUrl = 'http://{}/api/security/logout'.format(self.host, cookies=cookies)
        response = requests.post(logoutUrl)

        return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sdate', action='store', dest='start_date', default="None")
    parser.add_argument("--edate", action="store", dest="end_date", default="None")
    parser.add_argument("--vehicle-name", action="store", dest="vehicle_name", default="None")
    parser.add_argument("--parent-id", action="store", dest="parent_id", default="")
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

    download_obj = DownLoad(start_date, end_date, log_input.vehicle_name, \
                            output_path, log_input.parent_id)
    download_obj.mainLoop()

if __name__ == "__main__":
    main()
