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

import yaml

from sym.config import ConfigYAML
from sym.exceptions import FileExistsError
from sym.exceptions import FileNotFoundError


###
### API Functions
###
def init(args):
    """Initialize sym configuration

    Symlink's the sym configuration file to ~/.symconfig to a directory containing a git repo for management of system
    configuration. If directory does not already exist or is not a git repo, then the user will need to create a this
    directory and initialize it as a git repo before proceeding.

    Parameters:
        basedir - The base directory where your configuration git repo lives

    Returns:
        An integer representing error code
    """
    userhome = get_user_home()
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
        config.save()

    return True  # Success


def add(args):
    """Creates a symlink from a source path at a destination

    Creates a symlink, if the symlink already exists and verified pointing to the correct path then simply updates the
    database to ensure that the symlink is stored.

    Paths are stored as follows:
        - If absolute paths are passed, then the absolute paths will be stored in the database.
        - If a relative path is passed, and if the path is relative to the user's $HOME directory then a path relative
          to the user's $HOME will be saved instead.
        - If a relative path is passed that is not within the user's $HOME then the absolute path will be stored.

    Parameters:
        source      - The path to the source file in which to symlink to
        destination - The path to the location where to create the symlink
    """
    symconfig = get_symconfig_path()
    source = os.path.abspath(args.source)
    destination = os.path.abspath(args.destination)

    if not os.path.exists(source):
        raise FileNotFoundError('Source path does not exist: {}'.format(source))

    if os.path.lexists(destination):
        if not os.path.realpath(destination) == source:
            raise FileExistsError('Destination path exists, cannot create link at: {}'.format(destination))
        # else: Symlink exists but is already pointing to the correct path
    else:  # If destination path doesn't exist, proceed with creating the symlink
        os.symlink(source, destination)

    # Add or Update symlink in symlink database
    # Note: use path relative to $HOME or absolute path if provided by user
    save_source = source
    if args.source.startswith('/'):
        save_source = args.source
    elif source.startswith(get_user_home()):
        save_source = os.path.relpath(source, get_user_home())

    save_destination = destination
    if args.destination.startswith('/'):
        save_destination = args.destination
    elif args.destination.startswith(get_user_home()):
        save_destination = os.path.relpath(destination, get_user_home())

    config = load_config(symconfig)
    config.symlinks[save_destination] = save_source
    config.save()


def remove(args):
    print('remove')


def verify(args):
    print('verify')


###
### Helper functions
###
def get_user_home():
    """Returns the home directory of the user"""
    return os.path.expanduser(os.environ["HOME"])


def get_symconfig_path():
    """Returns the real path to .symconfig"""
    userhome = get_user_home()
    return os.path.realpath(os.path.join(userhome, '.symconfig'))


def load_config(symconfig):
    """Returns the symconfig object (ConfigYAML)

    Parameters:
        symconfig - The path to symconfig file

    Returns:
        Object containing symconfig (ConfigYAML)
    """
    stream = open(symconfig, 'r')
    config = yaml.load(stream)
    stream.close()
    return config
