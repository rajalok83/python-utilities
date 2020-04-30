from __future__ import print_function
import sys
import os
from time import sleep
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '{}'.format('..')))

from commons.jsonproc import JSONPROC

class PuttyOpener:
  in_file = None
  appName = None
  envName = None
  hostName = None
  userName = None
  def identify_server_id(self, in_path=None):
    if in_path is None or in_path == 'app' or in_path == '':
      look_for = 'app'
      in_path = 'app'
    else:
      #print(in_path.count('.'))
      if in_path.count('.') == 1:
        look_for = 'env'
      elif in_path.count('.') == 2:
        look_for = 'server'
        in_path += '.server'
      elif in_path.count('.') == 4:
        look_for = 'id'
        in_path='.'.join(in_path.split('.')[:-2])+'.id'
    print('Choose {} from below:'.format(look_for))
    #print(in_path)
    read_subset = self.read_json(in_path)
    read_choice = self.get_choice(self.print_array(read_subset), in_path)
    os.system('cls')
    if read_choice == -1:
      #print('Before'+in_path)
      if(in_path.count('.') == 3 and in_path.find('.id') == -1):
        in_path = '.'.join(in_path.split('.')[:-1])
      elif(in_path.count('.') == 3 and in_path.find('.server') > -1):
        in_path +='.x' 
      in_path = '.'.join(in_path.split('.')[:-1])
      #print('After'+in_path)
      self.identify_server_id(in_path)
    else:
      print('You chose:{}'.format(read_subset.keys()[read_choice]))
      if look_for == 'app':
        self.appName = read_subset.keys()[read_choice]
        self.envName = None
        self.hostName = None
        self.userName = None
      elif look_for == 'env':
        self.envName = read_subset.keys()[read_choice]
        self.hostName = None
        self.userName = None
      elif look_for == 'server':
        self.hostName = read_subset[read_subset.keys()[read_choice]]
      elif look_for == 'id':
        self.userName = read_subset[read_subset.keys()[read_choice]]
        print("Starting putty")
        #os.system("puTTy.exe ")
      #print('{}-{}-{}@{}'.format(self.appName, self.envName, self.userName, self.hostName))
      self.identify_server_id(in_path+'.'+read_subset.keys()[read_choice])
    return

  def get_choice(self, max_entry, in_path):
    try:
      response = raw_input("Please make a choice:")
      if response.upper() == 'B':
        return -1
      elif response.upper() == 'X':
        self.wait_and_exit(10, True)
      elif 0 <= int(response) <= max_entry:
        return int(response)
      else:
        print('Invalid choice, it can only benumeric value between 0 and {}. Please try again.'.format(max_entry))
        return self.get_choice(max_entry, in_path)
    except:
      print('Invalid choice, it can only benumeric value between 0 and {}. Please try again.'.format(max_entry))
      return self.get_choice(max_entry, in_path)
    return

  def wait_and_exit(self, n, is_exit):
    if is_exit:
      print('Exiting', end='')
    for i in range(n):
      print('.', end='')
      sleep(1)
    if is_exit:
      exit()
    return

  def print_array(self, in_arr):
    i = 0
    for xkey in in_arr:
      print('{}: {}'.format(i, xkey))
      i = i + 1
    print('{}: {}'.format('B', 'Back'))
    print('{}: {}'.format('X', 'Exit'))
    return i - 1

  def read_json(self, in_json_path):
    json_proc = JSONPROC(self.in_file)
    return json_proc.get_json_parm(in_json_path)

  def __init__(self, in_file):
    self.in_file = in_file
    return

if __name__ == '__main__':
  putty_opener = PuttyOpener('..\\conf\\uss_app_env_server_id.json')
  putty_opener.identify_server_id()
