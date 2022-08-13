
from os import getenv

class CheckInPath:
    def check_in_env_path(self, in_str, is_case_sensitive):
        source = getenv('path')
        if not is_case_sensitive:
            source = source.upper()
            in_str = in_str.upper()
        if source.find(in_str) > -1:
            return True
        else:
            return False
    
    def __init__(self):
        return

if __name__ == '__main__':
    proc = CheckInPath()
    proc.check_in_env_path('python')