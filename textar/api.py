import os
from uuid import uuid4
import ntpath
import sys
from .errors import (
    ArchiveExistsError,
    ArchiveNotFound,
    InvalidTextar,
    ExtractError
)


class Textar:

    def __init__(self, txr_file, input_files=[], cli=False):
        self._txr_file = txr_file
        self._boundary = uuid4().hex
        self._input_files = set(input_files)
        self._cli = cli

    def __repr__(self):
        return '<Textar : %s>' % self._txr_file

    @property
    def boundary(self):
        try:
            self._boundary, _ = self.validate_txr()
        except (InvalidTextar, ArchiveNotFound):
            self._boundary = ''
        return self._boundary

    @property
    def count(self):
        return len(self.list_archive())

    def add_file(self, input_file):
        pass

    def make_archive(self, overwrite=True):
        '''
        Make an archive of all the input files using the `txr_file` location
        '''

        if os.path.isfile(self._txr_file):
            if self._cli:
                print('*' * 25)
                print('An archive already exists under this name,'
                      ' this will be overwritten...')
                print('*' * 25)
                print('Archiving into %s ...' % self._txr_file)

            elif not overwrite:
                raise ArchiveExistsError(
                    'An archive already exists under this name')

        try:
            boundary = uuid4().hex

            with open(self._txr_file, 'w') as out:
                out.write('boundary: %s\n' % boundary)
                for input_file in self._input_files:
                    # Start of a file, add boundary line
                    filename = ntpath.basename(input_file)

                    boundary_line = '\n%s %s\n' % (boundary, filename)
                    out.write(boundary_line)

                    # Copy contents from input file
                    if self._cli:
                        print('Add file `%s` to archive' % filename)
                    try:
                        with open(input_file) as inp:
                            out.writelines(inp.readlines())
                    except FileNotFoundError as e:
                        os.remove(out_file)
                        if self._cli:
                            print(e)
                            print('Exiting ...')
                            sys.exit(0)
                        else:
                            raise
            return True
        except FileNotFoundError as e:
            if self._cli:
                print(e)
                print('Exiting ...')
                sys.exit(0)
            raise ArchiveNotFound(
                'The archive does not exist.') from e

    def validate_txr(self):
        '''
        Check if file is a valid txr (should start with key-val pair for
        boundary)

        Exits command if invalid for cli
        or
        Returns a tuple (boundary, content)
        '''
        boundary = content = ''
        try:
            with open(self._txr_file) as inp:
                content = inp.readlines()
                if content[0].startswith('boundary: '):
                    boundary = content[0].split(' ', 1)[-1].strip()
                else:
                    if self._cli:
                        print('File seems to be an invaild Textar file.')
                        print('Exiting ...')
                        sys.exit(0)
                    raise InvalidTextar(
                        '<File %s> is an invaild Textar file.' % self._txr_file)
            return boundary, content
        except FileNotFoundError as e:
            if self._cli:
                print(e)
                print('Exiting ...')
                sys.exit(0)
            else:
                raise ArchiveNotFound(
                    'The archive does not exist.') from e

    def list_archive(self):
        '''
        Find all the files the archive contains
        returns: list
        '''

        try:
            boundary, file_content = self.validate_txr()
        except (ArchiveNotFound, InvalidTextar):
            return []

        _files = []
        for line in file_content:
            if line.startswith(boundary):
                filename = line.split(' ', 1)[-1].strip()
                _files.append(filename)
        return _files

    def extract(self, extract_to=None):
        try:
            boundary, file_content = self.validate_txr()
        except ArchiveNotFound as e:
            raise ExtractError(e) from None if not self._cli else print(e)
        except InvalidTextar as e:
            raise e if not self._cli else print(e)

        # get current working dir
        if extract_to:
            try:
                os.mkdir(extract_to)
                cwd = extract_to
            except FileExistsError:
                cwd = extract_to
            except FileNotFoundError:
                if not self._cli:
                    raise ExtractError('A directory is required') from None
                else:
                    print('ExtractError : A directory is required')

        else:
            cwd = os.getcwd()

        # Clean the cwd for old extracted files if any

        for f in self.list_archive():
            try:
                os.remove(os.path.join(cwd, f))
            except FileNotFoundError:
                pass

        if self._cli:
            print('Extracting files into %s:\n' % cwd)

        # get boundary value
        new_file = None
        for line in file_content:
            if line.startswith(boundary):
                filename = line.split(' ', 1)[-1].strip()
                new_file = os.path.join(cwd, filename)
                if self._cli:
                    print(filename)
            elif new_file:
                with open(new_file, 'a') as out:
                    out.write(line)
        if self._cli:
            print('Extracted')
