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

import os
import tempfile
import unittest
import yaml

from sym.config import ConfigYAML


class TestConfig(unittest.TestCase):
    """Tests the configuration file format"""

    def setUp(self):
        self.configfile, self.configpath = tempfile.mkstemp()

    def tearDown(self):
        os.remove(self.configpath)

    def createConfig(self):
        stream = open(self.configpath, 'w')
        config = ConfigYAML()
        config.symlinks['~/git/dotfiles/testfile'] = '~/.testfile'
        config.symlinks['~/git/dotfiles/testconfig'] = '~/.testconfig'
        yaml.dump(config, stream)
        stream.close()

    def loadConfig(self):
        stream = open(self.configpath, 'r')
        config = yaml.load(stream)
        stream.close()
        return config

    def test_create_config(self):
        """Simply test that the config file was created"""
        self.createConfig()

    def test_load_config(self):
        """Simply test that the config file was created"""
        self.loadConfig()

    def test_read_symlinks(self):
        """Test reading the symlinks in a config"""
        self.createConfig()
        config = self.loadConfig()
        i = 0
        print('')  # Start on a new line
        for symlink in config.symlinks.items():
            print(i, ": ", symlink)
            i += 1
