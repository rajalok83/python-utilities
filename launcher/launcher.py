import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from commons import jsonproc


class Launcher:
  conf_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "..\\conf")
  conf_file = "launcher_connect.json"
  json_proc = None
  flows = None

  def run_function(self, func_index, in_data):
    func_typ = func_index.split("_")[0]
    func_nm = "{}_fn".format(func_typ)
    func = getattr(Launcher, func_nm)
    if func_typ == "list":
      func(self, func_index, func_index.replace("list_", "").replace(
        "_", "."), "Select {}".format(func_index.split("_")[-1].upper()))
    elif func_typ == "set":
      func(self, ('_').join(func_index.split('_')[1:-1]), in_data)
    elif func_typ == "setall":
      func(self, func_index.replace("setall_", "").replace("_", "."))
    elif func_typ == "run":
      all_vars = self.json_proc.get_json_parm("setv")
      for var_key in all_vars.keys():
        func_index = func_index.replace(
          var_key + "_key", str(all_vars.get(var_key)))
      func(self, func_index)
    return

  def print_suboptions(self, in_flow):
    all_options = self.json_proc.get_json_parm("flow.{}".format(in_flow))
    x = ""
    for key in all_options.keys():
      if key != "action":
        x += "{}: {} ".format(key, "Back" if key == 'B' else all_options[key])
    print(x)
    return all_options

  def set_json_path(self, in_json_path):
    in_json_path_arr = in_json_path.split('.')
    keys_arr = []
    while "key" in in_json_path_arr:
      val = getattr(
        Launcher, in_json_path_arr[in_json_path_arr.index("key") - 1])
      in_json_path_arr[in_json_path_arr.index("key")] = val
      keys_arr.append(val)
    return keys_arr, '.'.join(in_json_path_arr)

  def list_fn(self, in_flow, in_json_path, in_header):
    os.system("cls")
    keys_arr, in_json_path = self.set_json_path(in_json_path)
    print("You selected:{}".format(
      "->".join(keys_arr) if len(keys_arr) > 0 else ""))
    print(in_header)
    print("")
    all_keys = list(self.json_proc.get_json_parm(in_json_path).keys())
    # print(all_keys)
    for i in range(0, len(all_keys)):
      print("{}: {}".format("{} ".format(i) if i < 10 else i, all_keys[i]))
    print("")
    all_options = self.print_suboptions(in_flow)
    invalid_input = True
    while invalid_input:
      user_input = input("Choose an option: ")
      try:
        if 0 <= int(user_input) < len(all_keys):
          invalid_input = False
          for fn in self.json_proc.get_json_parm("flow.{}.action".format(in_flow)):
            self.run_function(fn, all_keys[int(user_input)])
      except:
        if user_input in all_options.keys() or user_input.upper() in all_options.keys():
          invalid_input = False
          if user_input.upper() == 'X':
            sys.exit(0)
    return

  def set_fn(self, in_nm, in_val):
    setattr(Launcher, in_nm, in_val)
    if(self.json_proc.add_kv("setv.{}".format(in_nm), in_val) == -1):
      print("Error setting variables in json")
      sys.exit(8)
    return

  def setall_fn(self, in_json_path):
    keys_arr, in_json_path = self.set_json_path(in_json_path)
    for key in self.json_proc.get_json_parm(in_json_path):
      val = self.json_proc.get_json_parm(
        "{}.{}".format(in_json_path, key))
      setattr(Launcher, key, val)
      if(self.json_proc.add_kv("setv.{}".format(key), val) == -1):
        print("Error setting variables in json")
        sys.exit(8)
    return

  def run_fn(self, in_json_path):
    all_vars = self.json_proc.get_json_parm("setv")
    oprns = self.json_proc.get_json_parm("flow.{}".format(in_json_path))
    full_txt = "cmd /k - new_console: t" if self.cli_env == "CONEMU" else "start cmd /c"
    for oprn in oprns:
      oprn_txt = self.json_proc.get_json_parm("syntax.{}".format(oprn))
      for var_key in all_vars:
        oprn_txt = oprn_txt.replace("{}{}{}".format(
          '%', var_key, "_key%"), str(all_vars.get(var_key)))
      full_txt = "{} {} {}".format(
        full_txt, '&', oprn_txt)
    print(full_txt)
    os.system("{} & PAUSE & EXIT".format(
      full_txt))
    return

  def __init__(self, in_file) -> None:
    if os.getenv("CONEMUBUILD") is None:
      self.cli_env = "cmd"
      print("You are not running in ConEmu")
    elif "$P$G" in os.getenv("CONEMUBUILD"):
      self.cli_env = "cmd"
      print("You are not running in ConEmu")
    else:
      self.cli_env = "CONEMU"
    if in_file is not None:
      if os.path.exists(in_file):
        self.conf_dir = os.path.dirname(os.path.abspath(in_file))
        self.conf_file = os.path.basename(in_file)
      else:
        print("File {} doesn't exists".format(in_file))
    else:
      pass
    self.json_proc = jsonproc.JSONProc(
      "{}\\{}".format(self.conf_dir, self.conf_file))
    self.flows = self.json_proc.get_json_parm("flow")
    return


if __name__ == "__main__":
  p1 = Launcher(sys.argv[1] if len(sys.argv) > 1 else None)
  while True:
    try:
      p1.run_function(p1.json_proc.get_json_parm("flow.start"), None)
    except KeyboardInterrupt:
      print("")
      print("Exiting..Good Bye..")
      p1.exit()
