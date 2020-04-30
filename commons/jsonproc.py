import json
import traceback
from collections import OrderedDict


class JSONPROC:
  in_file = None
  def get_json_parm(self, in_path):
    try:
      with open(self.in_file,  'r') as conf_file:
        conf_dict = json.load(conf_file, object_pairs_hook=OrderedDict)
        for path_node in in_path.split("."):
          try:
            conf_dict = conf_dict[path_node]
          except TypeError:
            return None
        return conf_dict
    except IOError:
      print(traceback.format_exc())
      exit()

  def __init__(self, in_file):
    self.in_file = in_file
    return
        
if __name__ == '__main__':
  json_proc = JSONPROC('..\\conf\\my_connect.json')
  x = json_proc.get_json_parm('cassandra.cqlsh.connect-parm')
  for xkey in x.keys():
    print(xkey)
