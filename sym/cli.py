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
import sys

from sym.api import add
from sym.api import init
from sym.api import remove
from sym.api import verify
from sym.exceptions import FileExistsError
from sym.exceptions import FileNotFoundError


def setup_parser_args(parser, subparsers):
    """Setup the main arguement parser"""
    setup_parser_init(subparsers)
    setup_parser_add(subparsers)
    setup_parser_remove(subparsers)
    setup_parser_verify(subparsers)


def setup_parser_init(subparsers):
    """Setup the init command parser"""
    parser_init = subparsers.add_parser('init', help='Initialize sym configuration')
    parser_init.add_argument('basedir', help='The base directory where your configuration git repo lives')
    parser_init.set_defaults(func=init)


def setup_parser_add(subparsers):
    """Setup the add command parser"""
    parser_add = subparsers.add_parser('add', help='Add dotfile for management')
    parser_add.add_argument('source')
    parser_add.add_argument('destination')
    parser_add.set_defaults(func=add)


def setup_parser_remove(subparsers):
    """Setup the remove command parser"""
    parser_remove = subparsers.add_parser('remove', help='Remove dotfile from management')
    parser_remove.add_argument('symlink')
    parser_remove.set_defaults(func=remove)


def setup_parser_verify(subparsers):
    """Setup the verify command parser"""
    parser_verify = subparsers.add_parser('verify', help='Verify dotfiles')
    parser_verify.set_defaults(func=verify)


def setup_parser():
    """Initialize the Argument Parser"""
    parser = argparse.ArgumentParser(description='Sym, dotfiles and configuration management tool')
    subparsers = parser.add_subparsers(dest='apicall', help='Command List')
    setup_parser_args(parser, subparsers)
    return parser


def parse_args(parser, parse_args=None, homedir='~'):
    args = parser.parse_args(parse_args)

    if args.apicall == 'init':
        try:
            args.func(args, homedir=homedir)
        except FileExistsError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)

    elif args.apicall == 'add':
        try:
            args.func(args, homedir=homedir)
        except FileExistsError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)

    elif args.apicall == 'remove':
        pass

    elif args.apicall == 'verify':
        pass
