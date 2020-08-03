#!/usr/bin/python
# -*- coding: utf-8 -*-
import linter

with open('./testFile.rb', 'r') as f:
    data = f.read()

res = linter.lint(data, 'testFile.rb')
print(res)