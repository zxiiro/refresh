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

from sym import api
from sym.config import ConfigYAML
from sym.exceptions import FileNotFoundError
from sym.exceptions import FileExistsError


class TestAPI(unittest.TestCase):
    """Tests the sym API"""

    def setUp(self):
        os.environ["HOME"] = tempfile.mkdtemp('homedir')
        self.homedir = os.environ["HOME"]
        self.testrepo = tempfile.mkdtemp('testrepo')

    def tearDown(self):
        shutil.rmtree(self.homedir)
        shutil.rmtree(self.testrepo)

    def test_api_init(self):
        """Test the init api"""
        sysconfig_path = os.path.join(self.homedir, '.symconfig')

        args = argparse.Namespace(basedir=self.testrepo)
        api.init(args)
        self.assertTrue(os.path.lexists(sysconfig_path))

        self.assertRaises(FileExistsError, api.init, args)  # Run a 2nd time to test existance condition

    def test_api_init_fake_basedir(self):
        """Test using an non-existant path"""
        fakepath = 'fakepath'
        fakeargs = argparse.Namespace(basedir=fakepath)
        self.assertRaises(FileNotFoundError, api.init, fakeargs)

    def test_api_init_relative_basedir(self):
        """Test relative path basedir"""
        sysconfig_path = os.path.join(self.homedir, '.symconfig')

        os.chdir(self.testrepo)
        reldir = 'test_relative_path'
        os.makedirs(reldir)
        relargs = argparse.Namespace(basedir=reldir)
        api.init(relargs)
        self.assertTrue(os.path.lexists(sysconfig_path))

    ###
    ### API Helper Functions
    ###
    def test_api_helper_get_user_home(self):
        """Test get_user_home() api"""
        userhome = api.get_user_home()
        self.assertEqual(userhome, self.homedir)

    def test_api_helper_get_symconfig_path(self):
        """Test get_symconfig_path() api"""
        args = argparse.Namespace(basedir=self.testrepo)
        api.init(args)

        symconfig = api.get_symconfig_path()
        symconfig_constructed = os.path.join(self.testrepo, 'symconfig')
        self.assertEqual(symconfig, symconfig_constructed)

    def test_api_helper_load_config(self):
        """Test loading_config() api"""
        args = argparse.Namespace(basedir=self.testrepo)
        api.init(args)
        symconfig = api.get_symconfig_path()
        config = api.load_config(symconfig)
        self.assertIsInstance(config, ConfigYAML)
