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

import argparse
import os
import shutil
import tempfile
import unittest

from sym import cli


class TestCLI(unittest.TestCase):
    """Tests the sym API"""

    def setUp(self):
        self.homedir = tempfile.mkdtemp()
        self.testrepo = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.homedir)
        shutil.rmtree(self.testrepo)

    def test_cli_help(self):
        """Test the CLI help functions"""
        parser = cli.setup_parser()
        with self.assertRaises(SystemExit) as cm:
            parser.parse_known_args(['-h'])

        parser = cli.setup_parser()
        with self.assertRaises(SystemExit) as cm:
            parser.parse_known_args('init -h'.split())

        parser = cli.setup_parser()
        with self.assertRaises(SystemExit) as cm:
            parser.parse_known_args('add -h'.split())

        parser = cli.setup_parser()
        with self.assertRaises(SystemExit) as cm:
            parser.parse_known_args('remove -h'.split())

        parser = cli.setup_parser()
        with self.assertRaises(SystemExit) as cm:
            parser.parse_known_args('verify -h'.split())

    def test_cli_init(self):
        """Test initializing a symconfig"""
        parser = cli.setup_parser()
        cli.parse_args(parser, ['init', self.testrepo], homedir=self.homedir)

    def test_cli_add(self):
        """Test adding symlinks"""
        parser = cli.setup_parser()
        cli.parse_args(parser, ['init', self.testrepo], homedir=self.homedir)

        #
        # Test successfully creating a link
        #
        test_path_a = os.path.join(self.testrepo, 'linkme')
        test_link_a = os.path.join(self.homedir, '.symlink')
        open(test_path_a, 'a').close()  # create file to link to

        cli.parse_args(parser, ['add', test_path_a, test_link_a], homedir=self.homedir)
        self.assertTrue(os.path.exists(test_link_a))

        #
        # Test creating a link to a destination that exists
        #
        test_path_b = os.path.join(self.testrepo, 'linkme_2')
        open(test_path_b, 'a').close()  # create file to link to
        cli.parse_args(parser, ['add', test_path_b, test_link_a], homedir=self.homedir)
        self.assertNotEqual(test_path_b, test_link_a)

        #
        # Test creating a link to a source that does not exist
        #
        test_path_c = os.path.join(self.testrepo, 'linkme_3')
        cli.parse_args(parser, ['add', test_path_c, test_link_a], homedir=self.homedir)
        self.assertFalse(os.path.exists(test_path_c))

        #
        # Test symlinking using absolute paths
        #
        tmp_abs_file, tmp_abs_path = tempfile.mkstemp()
        test_path_d = os.path.join(self.testrepo, 'linkme_abs')
        cli.parse_args(parser, ['add', tmp_abs_path, test_path_d], homedir=self.homedir)
        self.assertTrue(os.path.exists(test_path_d))

        #
        # Test symlinking using relative paths (to homedir)
        #
        tmp_abs_file, tmp_abs_path = tempfile.mkstemp(dir=self.homedir)
        test_path_d = os.path.join(self.homedir, 'linkme_rel')
        cli.parse_args(parser, ['add', tmp_abs_path, test_path_d], homedir=self.homedir)
        self.assertTrue(os.path.exists(test_path_d))

        #
        # Test symlinking using relative paths (to testrepo)
        #
        os.chdir(self.testrepo)
        tmp_abs_file, tmp_abs_path = tempfile.mkstemp(dir=self.testrepo)
        test_path_d = os.path.join(self.testrepo, 'linkme_rel_testrepo')
        cli.parse_args(parser, ['add', tmp_abs_path, test_path_d], homedir=self.homedir)
        self.assertTrue(os.path.exists(test_path_d))
