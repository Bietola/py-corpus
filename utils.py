import sys
import subprocess
from pathlib import Path
import os
from inspect import getsourcefile
import time

SRC_PATH = Path(os.path.abspath(getsourcefile(lambda:0))).parent

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def shell(*args):
    return subprocess.check_output(*args, shell=True)

def wait_until_connected(delay, trace=False):
    import urllib.request

    def try_connect(host='http://google.com'):
        try:
            urllib.request.urlopen(host) #Python 3.x
            return True
        except:
            return False

    while True:
        if try_connect():
            print('Connection successful!')
            return
        else:
            print(f'Connection failed... checking again in {delay}s')
            time.sleep(delay)

def unique_file_path(parent_dir, fstr='{}'):
    if not parent_dir.is_dir():
        return None

    j = 0
    while True:
        name = '{}-{}'.format(
            time.strftime('%Y-%m-%d', time.localtime()),
            j
        )
        name = fstr.format(name)
        path = parent_dir / Path(name)
        if not path.is_file():
            return path
        else:
            j += 1
            continue

