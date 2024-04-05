import os
import shutil
import time

import subprocess

current_dir = os.path.dirname(os.path.realpath(__file__))
print(current_dir)
node_odm = subprocess.Popen(['node', 'index.js', '--port', '11223'], shell=False,
                                cwd=os.path.join(current_dir, "nodeodm", "external", "NodeODM"))
