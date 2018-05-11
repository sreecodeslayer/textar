'''
CLI
'''

import argparse
import sys
from .api import Textar


def create_parser():
    parser = argparse.ArgumentParser(
        prog='textar', add_help=True, description='Textar is a simple and readable archive format')

    parser.add_argument('out_file', nargs='?',
                        help='Please provide a valid filepath for output archive')
    parser.add_argument('file_list', nargs='*',
                        help='Please provide a valid filepath(s)')
    parser.add_argument(
        '-l', '--list', help='Please provide a valid textar (.txr) file')
    parser.add_argument(
        '-x', '--extract', help='Please provide a valid textar (.txr) file to extract')

    return parser


def cli(args=sys.argv[1:]):
    parser = create_parser()
    args = parser.parse_args(args)

    if not args:
        parser.print_help()
        return

    if args.list:
        txr = Textar(args.list, cli=True)

        txr.list_archive()
    elif args.extract:
        txr = Textar(args.extract, cli=True)
        txr.extract()
    else:
        txr = Textar(args.out_file, input_files = args.file_list, cli=True)
        txr.make_archive()
