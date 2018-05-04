'''
CLI
'''

import argparse
import sys
from .api import (
    make_archive,
    extract
)

def create_parser():
    parser = argparse.ArgumentParser(
        prog='textar', add_help=False, description='Textar is a simple and readable archive format')

    parser.add_argument('out_file', help='Please provide a valid filepath for output archive')
    parser.add_argument('file_list', nargs='+', help='Please provide a valid filepath(s)')

    return parser

def cli(args=sys.argv[1:]):
    parser = create_parser()
    args = parser.parse_args(args)

    if not args:
        parser.print_help()
        return
    make_archive(args)