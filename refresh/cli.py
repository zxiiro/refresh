# -*- coding: utf-8 -*-

'''
  The MIT License (MIT)

  Copyright (c) 2013 Thanh Ha

  Permission is hereby granted, free of charge, to any person obtaining a copy of
  this software and associated documentation files (the "Software"), to deal in
  the Software without restriction, including without limitation the rights to
  use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
  the Software, and to permit persons to whom the Software is furnished to do so,
  subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
  FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
  IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
  CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import argparse


def setup_parser_args(parser):
    '''Add arguments to parse'''
    parser.add_argument('--add',
        help='Add dotfile for management',
        action='store_true')
    parser.add_argument('--remove',
        help='Remove dotfile from management',
        action='store_true')
    parser.add_argument('--check',
        help='Check dotfile link',
        action='store_true')


def parse_args():
    '''Initialize the Argument Parser'''
    parser = argparse.ArgumentParser(description='Refresh, dotfiles management tool')
    setup_parser_args(parser)
    args = parser.parse_args()


def main():
    parse_args()


if __name__ == '__main__':
    main()
