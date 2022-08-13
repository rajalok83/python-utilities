from __future__ import print_function

import os
import sys
from time import sleep

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '{}'.format('..')))

from commons.jsonproc import JSONProc

curr_py_ver = sys.version.split(' ')[0].split('.')[0]


class PuttyOpener:
    in_file = None
    appName = None
    envName = None
    hostName = None
    userName = None
    choice_str = None

    def identify_server_id(self, in_path=None):
        if in_path is None or in_path == 'app' or in_path == '':
            os.system('cls')
            look_for = 'app'
            in_path = 'app'
        else:
            # print(in_path.count('.'))
            if in_path.count('.') == 1:
                look_for = 'env'
            elif in_path.count('.') == 2:
                look_for = 'server'
                in_path += '.server'
            elif in_path.count('.') == 4:
                look_for = 'id'
                in_path = '.'.join(in_path.split('.')[:-2]) + '.id'
        print('Choose {} from below:'.format(look_for))
        # print(in_path)
        read_subset = self.read_json(in_path)
        read_choice = self.get_choice(self.print_array(read_subset), in_path)
        os.system('cls')
        if read_choice == -1:
            # print('Before'+in_path)
            if in_path.count('.') == 3  and in_path.find('.id') == -1:
                in_path = '.'.join(in_path.split('.')[:-1])
            elif in_path.count('.') == 3 and in_path.find('.server') > -1:
                in_path += '.x'
            self.choice_str = '->'.join(self.choice_str.split('->')[:-1])
            in_path = '.'.join(in_path.split('.')[:-1])
            # print('After'+in_path)
            if self.choice_str is not None:
                print(self.choice_str)
            self.identify_server_id(in_path)
        else:
            # print('You chose:{}'.format(read_subset.keys()[read_choice]))
            if look_for == 'app':
                self.appName = list(read_subset.keys())[read_choice]
                self.envName = None
                self.hostName = None
                self.userName = None
                self.choice_str = 'You chose:{}'.format(self.appName)
            elif look_for == 'env':
                self.envName = list(read_subset.keys())[read_choice]
                self.hostName = None
                self.userName = None
                self.choice_str = 'You chose:{}->{}'.format(self.appName, self.envName)
            elif look_for == 'server':
                # self.hostName = read_subset[list(read_subset.keys())[read_choice]]
                self.hostName = self.get_server(read_subset[read_choice])
                self.choice_str = 'You chose:{}->{}->{}'.format(self.appName, self.envName, self.hostName)
            elif look_for == 'id':
                if list(read_subset.keys())[read_choice] == "personal":
                    self.userName = os.getenv('username').lower()
                else:
                    self.userName = read_subset[list(read_subset.keys())[read_choice]]
                self.choice_str = 'You chose:{}->{}->{}@{}'.format(self.appName, self.envName, self.userName,
                                                                   self.hostName)
                print("Starting putty")
                pwd = self.get_pwd(self.userName)
                if pwd is None:
                    os.system("puTTy.exe -new_console:t{}@{}-{}-{} -ssh {}@{}".format(self.userName, self.hostName,
                    self.appName, self.envName, self.userName, self.hostName))
                else:
                    os.system("puTTy.exe -new_console:t{}@{}-{}-{} -ssh {}@{} -pw {}".format(self.userName, self.hostName,
                    self.appName, self.envName, self.userName, self.hostName, pwd))
            # print('{}-{}-{}@{}'.format(self.appName, self.envName, self.userName, self.hostName))
            if self.choice_str is not None:
                print(self.choice_str)
            if look_for == 'server':
                self.hostName = self.get_server(read_subset[read_choice])
                self.identify_server_id(in_path+'.'+read_subset[read_choice])
            else:
                self.identify_server_id(in_path + '.' + list(read_subset.keys())[read_choice])
        return

    def get_pwd(self, userName):
        json_proc = JSONProc(self.in_file)
        return json_proc.get_json_parm('{}.{}'.format('pwd', userName))

    def get_server(self, serverName):
        json_proc = JSONProc(self.in_file)
        return json_proc.get_json_parm('{}.{}'.format('servers', serverName))

    def get_choice(self, max_entry, in_path):
        try:
            if curr_py_ver == "2":
                response = (raw_input("Please make a choice:")).strip()
            else:
                response = (input("Please make a choice:")).strip()
            if response.upper() == 'B':
                return -1
            elif response.upper() == 'X':
                self.wait_and_exit(10, True)
                os._exit(8)
            elif 0 <= int(response) <= max_entry:
                return int(response)
            else:
                print(
                    'Invalid choice, it can only be numeric value between 0 and {}. Please try again.'.format(max_entry))
                return self.get_choice(max_entry, in_path)
        except:
            print('Invalid choice, it can only be numeric value between 0 and {}. Please try again.'.format(max_entry))
            return self.get_choice(max_entry, in_path)
        return

    def wait_and_exit(self, n, is_exit):
        if is_exit:
            print('Exiting', end='')
        for i in range(n):
            print('.', end='')
            sleep(1)
        if is_exit:
            os._exit(8)
        return

    def print_array(self, in_arr):
        i = 0
        for xkey in in_arr:
            print('{}: {}'.format(i, xkey))
            i = i + 1
        print('{}: {}'.format('B', 'Back') + ' {}: {}'.format('X', 'Exit'))
        return i - 1


    def read_json(self, in_json_path):
        json_proc = JSONProc(self.in_file)
        return json_proc.get_json_parm(in_json_path)

    def __init__(self, in_file):
        self.in_file = in_file
        return


if __name__ == '__main__':
    putty_opener = PuttyOpener('conf\\uss_app_env_server_id.json')
    putty_opener.identify_server_id()
