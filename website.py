import shutil
import glob
import os
import subprocess
import git

def create_web_journal(file):
    os.chdir("/awesomeDiary")
files = []
for file in glob.glob("*.md"):
    files.append(file)

for f in files:
    shutil.copy(f, '/data')

