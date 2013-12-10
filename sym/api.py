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

from sym.config import ConfigYAML
from sym.exceptions import FileExistsError
from sym.exceptions import FileNotFoundError


def init(args, homedir='~'):
    """Initialize sym configuration

    Symlink's the sym configuration file to ~/.symconfig to a directory containing a git repo for management of system
    configuration. If directory does not already exist or is not a git repo, then the user will need to create a this
    directory and initialize it as a git repo before proceeding.

    Parameters:
        basedir - The base directory where your configuration git repo lives

    Returns:
        An integer representing error code
    """
    userhome = os.path.expanduser(homedir)
    symconfig = os.path.join(userhome, '.symconfig')
    msg = ''

    # figure out if the path is absolute or relative or if it doesn't exist
    if os.path.isabs(args.basedir):  # is an absolute path
        symconfig_basepath = os.path.join(args.basedir, 'symconfig')
    elif os.path.exists(args.basedir):  # is a relative path, convert to absolute path
        symconfig_basepath = os.path.join(os.path.abspath(args.basedir), 'symconfig')
    else:
        raise FileNotFoundError('Failed to initialize symconfig, the path {} is not a valid path.'.format(args.basedir))

    #
    # Create the symbolic link
    #
    if os.path.lexists(symconfig):
        raise FileExistsError('Symlink for {0} already exists and links to {0}'.format(os.path.realpath(symconfig)))
    else:
        os.symlink(symconfig_basepath, symconfig)

    #
    # Craete real symconfig file if it doesn't exist in the repo
    #
    if not os.path.exists(symconfig_basepath):
        config = ConfigYAML()
        config.save(homedir=userhome)

    return True  # Success


def add(args):
    print('add')


def remove(args):
    print('remove')


def verify(args):
    print('verify')
