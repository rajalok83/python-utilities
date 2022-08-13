import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from commons.jsonproc import JSONPROC

class Crypto:
    in_string = None
    in_file = None

    def encrypt_base64(self, new_file=None, new_string=None):
        jsonproc = JSONPROC(new_file)
        key = jsonproc.get_json_parm("encryption_key")
        if key is None:
            key = ""
        if new_string is None:
            return (self.in_string+key).encode("base-64", "strict")
        else:
            return (self.new_string+key).encode("base-64", "strict")

    def decrypt_base64(self, new_file=None, new_string=None):
        jsonproc = JSONPROC(new_file)
        key = jsonproc.get_json_parm("encryption_key")
        if key is None:
            len_key = 0
        else:
            len_key = len(key)
        if new_string is None:
            return (self.in_string).decode("base-64")[0:-len_key]
        else:
            return (self.new_string).decode("base-64")[0:-len_key]
        # else:
        #     if new_string is None:
        #         return (self.in_string).decode("base-64")[0:-len(key)]
        #     else:
        #         return (self.new_string).decode("base-64")[0:-len(key)]

    def __init__(self, in_file, in_string):
        self.in_file = in_file
        self.in_string = in_string
        return

    def __init__(self):
        return

if __name__ == '__main__' :
    file_name = '..\\conf\\my_connect.json'
    user_name = raw_input("Please provide username:")
    password = raw_input("Please provide password:")
    c1 = Crypto()
    encrypted = c1.encrypt_base64(user_name+":"+password)
    print("Encrypted value(base64):{}".format(encrypted))
    print("Decrypted value(base64):{}".format(c1.decrypt_base64(encrypted)))
    json_proc = JSONPROC(file_name)
    json_proc.add_kv("cassandra.cqlsh.pwd.{}".format(user_name), encrypted)
    print("Password saved in {}".format(file_name))