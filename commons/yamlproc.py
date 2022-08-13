import yaml
import traceback
import json

class YAMLProc:
    in_file = None
    def get_yaml_parm(self, in_path):
        try:
            with open(self.in_file, 'r') as conf_file:
                conf_dict = yaml.load(conf_file)
                for path_node in in_path.split("."):
                    try:
                        conf_dict = conf_dict[path_node]
                    except TypeError:
                        return None
                return conf_dict
        except IOError:
            print(traceback.format_exc)
            exit()

    def to_json(self, out_file):
        with open(self.in_file, 'r') as yaml_in, open(out_file, 'w') as json_out:
            yaml_object = yaml.safe_load(yaml_in)
            json_out.write(json.dumps(yaml_object, indent=2, sort_keys=False))
            json_out.close()
        return

    def __init__(self, in_file):
        self.in_file = in_file
        return

if __name__ == "__main__":
    yaml_proc = YAMLProc('..\\conf\\API_Specification_1.0.yaml')
    yaml_proc.to_json('..\\conf\\GOS_API_SPECS.json')