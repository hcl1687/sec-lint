#!/usr/bin/python
# -*- coding: utf-8 -*-
import custom_hooks.linter

fileName = './testFile.rb'
with open(fileName, 'r') as f:
    data = f.readlines()

if custom_hooks.linter.isTarget(fileName):
    res = custom_hooks.linter.lint(data, 'testFile.rb')
    print(res)