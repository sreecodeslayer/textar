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

def extract(txr):
    pass
