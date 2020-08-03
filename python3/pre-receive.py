#!/usr/bin/python
import sys
import re
import subprocess
import linter

errorMsgs = []
line = sys.stdin.read()
(old, new, branch) = line.strip().split()

diffCommand = 'git diff --name-status ' + old + ' ' + new
proc = subprocess.Popen(diffCommand, stdout=subprocess.PIPE)
lines = proc.stdout.readlines()
if lines:
    for line in lines:
        # line = 'M    readme.txt'
        parts = re.split(r'\s+', str(line))
        if parts[0] != 'D':
            showCommand = 'git show ' + new + ':' + parts[1]
            proc = subprocess.Popen(showCommand, stdout=subprocess.PIPE)
            fileData = proc.stdout.readlines()
            errorMsgs = errorMsgs + linter.lint(fileData, parts[1])

if len(errorMsgs) == 0:
    exit(0)
else:
    for msg in errorMsgs:
        print(msg)
    exit(1)
