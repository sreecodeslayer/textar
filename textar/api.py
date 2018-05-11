import os
from uuid import uuid4
import ntpath
import sys
from .errors import (
    ArchiveExistsError,
    ArchiveNotFound,
    InvalidTextar
)


class Textar:

    def __init__(self, txr_file, input_files=[], cli=False):
        self.txr_file = txr_file
        self._boundary = uuid4().hex
        self._input_files = set(input_files)
        self.cli = cli
        self.validate_txr()

    def __repr__(self):
        return '<Textar : %s>' % self.txr_file

    @property
    def boundary(self):
        return self._boundary

    @property
    def count(self):
        return len(self.list_archive())

    def make_archive(self, overwrite=True):

        if os.path.isfile(self.txr_file):
            if self.cli:
                print('*' * 25)
                print('An archive already exists under this name,'
                      ' this will be overwritten...')
                print('*' * 25)
                print('Archiving into %s ...' % self.txr_file)

            elif not overwrite:
                raise ArchiveExistsError(
                    'An archive already exists under this name')

        try:
            with open(self.txr_file, 'w') as out:
                out.write('boundary: %s\n\n' % self.boundary)
                for input_file in self._input_files:
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

    def validate_txr(self):
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
                    if self.cli:
                        print('File seems to be an invaild Textar file.')
                        print('Exiting ...')
                        sys.exit(0)
                    raise InvalidTextar(
                        '<File %s> is an invaild Textar file.' % self.txr_file)
            return boundary, content
        except FileNotFoundError as e:
            if self.cli:
                print(e)
                print('Exiting ...')
                sys.exit(0)
            else:
                raise ArchiveNotFound(
                    'The archive does not exist.') from e


    def list_archive(self):
        boundary, file_content = self.validate_txr()

        # get boundary value
        _files = []
        for line in file_content:
            if line.startswith(boundary):
                filename = line.split(' ', 1)[-1].strip()
                if self.cli:
                    print(filename)
                else:
                    _files.append(filename)
        return _files


    def extract(self, extract_to=None, cli=False):

        boundary, file_content = self.validate_txr()

        # get current working dir
        cwd = extract_to if extract_to else os.getcwd() 
        
        if self.cli:
            print('Extracting files into %s:\n' % cwd)

        # get boundary value
        new_file = None
        for line in file_content:
            if line.startswith(boundary):
                filename = line.split(' ', 1)[-1].strip()
                new_file = os.path.join(cwd, filename)
                if self.cli:
                    print(filename)
            elif new_file:
                with open(new_file, 'a') as out:
                    out.write(line)
        if cli:
            print('Extracted')
