import json
import traceback
from collections import OrderedDict
import os

class JSONProc:
    in_file = None
    conf_dir = (os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\\conf"))
    
    def get_json_parm(self, in_path):
        # print(os.path.abspath(self.in_file))
        try:
            with open(self.in_file,  'r') as conf_file:
                conf_dict = json.load(conf_file, object_pairs_hook=OrderedDict)
                for path_node in in_path.split("."):
                    try:
                        conf_dict = conf_dict[path_node]
                    except (TypeError, KeyError):
                        return None
                return conf_dict
        except IOError:
            print(traceback.format_exc())
            exit()

    def add_kv(self, key, value):
        with open(self.in_file, 'r') as file_to_read:
            complete_json_info = json.load(
                file_to_read, object_pairs_hook=OrderedDict)
            json_info = complete_json_info
            all_keys = key.split(".")
            i = 0
            for i in range(len(all_keys)):
                path_node = all_keys[i]
                if i == len(all_keys) - 1:
                    json_info[path_node] = value
                else:
                    try:
                        json_info = json_info[path_node]
                    except TypeError:
                        return None
                    except KeyError:
                        if i == len(all_keys) - 1:
                            json_info[path_node] = value
                        else:
                            json_info[path_node] = {}
                        json_info = json_info[path_node]
            try:
                with open(self.in_file) as file_to_write:
                    file_to_write.write(json.dumps(
                        complete_json_info, indent=4))
                    file_to_write.close()
                    return 0
            except:
                return -1

    def __init__(self, in_file):
        self.in_file = in_file
        return


def get_json_parm(in_file, in_path):
    json_proc = JSONProc(in_file)
    return json_proc.get_json_parm(in_path)


if __name__ == '__main__':
    json_proc = JSONProc("conf\\connect.json")
    x = json_proc.get_json_parm('cassandra.cqlsh.connect-parm')
    for xkey in x.keys():
        print(xkey)
