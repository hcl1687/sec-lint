#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import re
import StringIO


'''
load rules object from rules directory and precompile the regular expression string.
ruleObj = {
    target: '.+\\.rb$',  # regular expression string, using to match the target file name.
    rules: [{
        "rule": "params.permit!",  # regular expression string, using to match the dangerous commands.
        "message": "params.permit is dangerous"  # string, will be printed for each occurrence of the problem
    }, {
        "rule": "map.connect \":controller/:action/:id\"",
        "message": "map.connect is dangerous"
    }]
}
'''
def loadRules():
    path = './rules'
    ruleObjList = []
    for ruleFileName in os.listdir(path):
        # open json file and load data.
        with open(path + '/' + ruleFileName, 'r') as f:
            ruleObj = json.load(f)

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
