#!/usr/bin/python
import sys
import re
import subprocess
import json
import os
import StringIO

RULE_OBJ_LIST = [{
    "target": ".+\\.rb$",
    "rules": [{
        "rule": "params.permit!",
        "message": "params.permit is dangerous"
    }, {
        "rule": "map.connect \":controller/:action/:id\"",
        "message": "map.connect is dangerous"
    }, {
        "rule": "match \":controller(/:action(/:id(.:format)))\"",
        "message": "match is dangerous"
    }, {
        "rule": "map.connect",
        "message": "map.connect is dangerous"
    }, {
        "rule": "match \":",
        "message": "match is dangerous"
    }]
}]

# errorMsgs = []
# line = sys.stdin.read()
# (old, new, branch) = line.strip().split()

# diffCommand = 'git diff --name-status ' + old + ' ' + new
# proc = subprocess.Popen(diffCommand, stdout=subprocess.PIPE)
# lines = proc.stdout.readlines()
# if lines:
#     for line in lines:
#         # line = 'M    readme.txt'
#         parts = re.split(r'\s+', str(line))
#         if parts[0] != 'D':
#             showCommand = 'git show ' + new + ':' + parts[1]
#             proc = subprocess.Popen(showCommand, stdout=subprocess.PIPE)
#             fileData = proc.stdout.readlines()
#             errorMsgs = errorMsgs + linter.lint(fileData, parts[1])

# if len(errorMsgs) == 0:
#     exit(0)
# else:
#     for msg in errorMsgs:
#         print(msg)
#     exit(1)

def loadRules():
    path = './rules'
    ruleObjList = []
    # for ruleFileName in os.listdir(path):
    #     with open(path + '/' + ruleFileName, 'r') as f:
    #         ruleObj = json.load(f)
    for ruleObj in RULE_OBJ_LIST:
        # precompile regex
        if ruleObj.get('target') == None:
            continue
        ruleObj['regex'] = re.compile(ruleObj['target'])

        regexObjList = ruleObj.get('rules')
        if regexObjList == None:
            continue

        for regexObj in regexObjList:
            if regexObj.get('rule') == None:
                continue
            regexObj['regex'] = re.compile(regexObj['rule'])
            if regexObj.get('message') == None:
                regexObj['message'] = ''

        ruleObjList.append(ruleObj)

    return ruleObjList

def lint(fileData, fileName):
    ruleObjList = loadRules()
    res = []

    if len(fileData) == 0:
        return res

    # filter rules based on fileName
    ruleObjList = list(filter(lambda ruleObj: ruleObj['regex'].match(fileName), ruleObjList))
    if len(ruleObjList) == 0:
        return res

    f = StringIO.StringIO(fileData)
    lineNo = 1
    while True:
        lineData = f.readline()
        if lineData == '':
            break

        errs = lintLine(lineData, ruleObjList, lineNo, fileName)
        if (len(errs) > 0):
            res = res + errs
        lineNo = lineNo + 1
    
    print(res)

    return res

def lintLine(lineData, ruleObjList, lineNo, fileName):
    res = []
    for ruleObj in ruleObjList:
        regexObjList = ruleObj['rules']
        for regexObj in regexObjList:
            if regexObj.get('regex') == None:
                continue

            search = regexObj['regex'].search(lineData)
            if search == None:
                continue

            message = regexObj['message']
            res.append(message + ' in ' + fileName + '(line:' + str(lineNo) + ')')

    return res