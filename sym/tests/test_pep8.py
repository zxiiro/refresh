#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  The MIT License (MIT)
#
#  Copyright (c) 2013 Thanh Ha
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of
#  this software and associated documentation files (the "Software"), to deal in
#  the Software without restriction, including without limitation the rights to
#  use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
#  the Software, and to permit persons to whom the Software is furnished to do so,
#  subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
#  FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
#  IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
#  CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest

import pep8

pep8_options = {'max_line_length': 120,
                'ignore': ['E127',   # Ignore over indents
                           'E128',   # Ignore under indents
                           'E221',   # Multiple whitespace before operator
                           'E241']}  # Ignore multiple whitespaces after :


def pep8_report(test, report):
    output = ''
    for line in report.get_statistics(''):
        output += '\t%s\n' % line

    test.assertEqual(report.total_errors, 0,
                     "Found %s code style errors (and warnings):\n\n%s" % (report.total_errors, output))


class TestCode(unittest.TestCase):
    def test_pep8(self):
        '''Test that sym code conforms to pep8'''
        checker = pep8.StyleGuide(**pep8_options)
        report = checker.check_files(['sym'])
        pep8_report(self, report)
