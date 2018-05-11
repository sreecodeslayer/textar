import os
from uuid import uuid4
import ntpath
import sys
from .errors import (
    ArchiveExistsError
    ArchiveNotFound
)


class Textar:
    def __init__(self, txr_file=None, input_files=[]):
        self.txr_file = txr_file
        self._boundary = uuid4().hex
        self._input_files = set(input_files)

    def __repr__(self):
        return '<Textar : %s>' % self.txr_file

    @property
    def boundary(self):
        return self._boundary

    @property
    def count(self):
        return len(self._input_files)

    def list_archive(self):
        boundary, file_content = self.validate_txr()

        # get boundary value
        for line in file_content:
            if line.startswith(boundary):
                filename = line.split(' ', 1)[-1].strip()
                print(filename)

    def make_archive(self, out, files, overwrite=True, cli=False):
        '''
        Takes in a parsed args instance of ArgumentParser
        '''
        # Get out file
        self.out_file = out

        # Get list of files to archive
        input_files = files

        if os.path.isfile(self.out_file):
            if cli:
                print('*' * 25)
                print('An archive already exists under this name,'
                      ' this will be overwritten...')
                print('*' * 25)
                overwrite = False
                print('Archiving into %s ...' % out_file)

            if not overwrite:
                raise ArchiveExistsError(
                    'An archive already exists under this name')

        try:
            with open(self.out_file, 'w') as out:
                out.write('boundary: %s\n\n' % self.boundary)
                for input_file in input_files:
                    # Start of a file, add boundary line
                    filename = ntpath.basename(input_file)

                    boundary_line = '%s %s\n' % (self.boundary, filename)
                    out.write(boundary_line)

                    # Copy contents from input file
                    print('Add file `%s` to archive' % filename)
                    try:
                        with open(input_file) as inp:
                            out.writelines(inp.readlines())
                    except FileNotFoundError as e:
                        print(e)
                        os.remove(out_file)
                        print('Exiting ...')
                        sys.exit(0)
                else:
                    return False
            return True
        except FileNotFoundError as e:
            print(e)
            print('Exiting ...')
            sys.exit(0)

    def validate_txr(self, cli=False):
        '''
        check if file is a valid txr (should start with key-val pair for
        boundary)

        Exits command if invalid for cli
        or
        Returns a tuple (boundary, content)
        '''
        boundary = content = ''
        try:
            with open(self.txr_file) as inp:
                content = inp.readlines()
                if content[0].startswith('boundary: '):
                    boundary = content[0].split(' ', 1)[-1].strip()
                else:
                    if cli:
                        print('File seems to be an invaild Textar file.')
                        print('Exiting ...')
                        sys.exit(0)
            return boundary, content
        except FileNotFoundError as e:
            if cli:
                print(e)
                print('Exiting ...')
                sys.exit(0)
            else:
                raise ArchiveNotFound('The archive does not exist. Please provide a correct path')


def list_archive(txr_file):
    boundary, file_content = validate_txr(txr_file)

    # get boundary value
    for line in file_content:
        if line.startswith(boundary):
            filename = line.split(' ', 1)[-1].strip()
            print(filename)


def extract(txr_file):

    boundary, file_content = validate_txr(txr_file)

    # get current working dir
    cwd = os.getcwd()
    print('Extracting files into %s:\n' % cwd)

    # get boundary value
    new_file = None
    for line in file_content:
        if line.startswith(boundary):
            filename = line.split(' ', 1)[-1].strip()
            new_file = os.path.join(cwd, filename)
            print(filename)
        elif new_file:
            with open(new_file, 'a') as out:
                out.write(line)
    print('Extracted')
