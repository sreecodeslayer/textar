import os
from uuid import uuid4
import ntpath
import sys

def make_archive(args):
    '''
    Takes in a parsed args instance of ArgumentParser
    '''
    # Get out file
    out_file = args.out_file

    # Get list of files to archive
    input_files = args.file_list

    if os.path.isfile(out_file):
        print('*'*25)
        print('An archive already exists under this name, this will be overwritten...')
        print('*'*25)

    print('Archiving into %s ...' % out_file)

    boundary = uuid4().hex
    with open(out_file, 'w') as out:
        out.write('boundary: %s\n\n' % boundary)
        for input_file in input_files:
            # Start of a file, add boundary line
            filename = ntpath.basename(input_file)

            boundary_line = '%s %s\n' % (boundary,filename)
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

def list_archive(txr_file):
    try:
        with open(txr_file) as inp:
            file_content = inp.readlines()
            # check if file is a valid txr (should start with key-val pair for boundary)
            if file_content[0].startswith('boundary: '):
                boundary = file_content[0].split(' ',1)[-1].strip()
            else:
                print('File seems to be an invaild Textar file.')
                print('Exiting ...')
                sys.exit(0)

            # get boundary value
            for line in file_content:
                if line.startswith(boundary):
                    filename = line.split(' ', 1)[-1].strip()
                    print(filename)
    except FileNotFoundError as e:
        print(e)
        print('Exiting ...')
        sys.exit(0)

def extract(txr):
    pass
