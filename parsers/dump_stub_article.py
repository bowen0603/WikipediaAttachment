__author__ = 'bobo'

from mw.xml_dump import Iterator
from mw.xml_dump import functions

###############################################################
## Code Description
##
## the code take in one stub meta article file as input for parsing.
## it will get the title, page id, and namespace of each page/article on wikipedia
##
###############################################################
## Revision Records
## record = {"page_title": page.title, "page_id": page.id, "ns":page.namespace}
##
###############################################################
## Input files: <input_file> <output_file>
## dump meta current page file; output file name with file type
##

def parse_file(input=None, output=None):

    fout = open(output, 'w')
    dump = Iterator.from_file(functions.open_file(input))

    for page in dump:
        # ignore old version pages that were redirected
        if page.redirect:
            continue

        record = {"page_title": page.title, "page_id": page.id, "ns": page.namespace}
        from json import dumps
        print(dumps(record), file=fout)


def main(argv=None):
    # give the input and output filenames, wp and cat data will be parsed into different folders
    if len(argv) != 3:
        print("usage: <input_file> <output_file>")
        return

    parse_file(input=argv[1], output=argv[2])

if __name__ == '__main__':
    from sys import argv
    main(argv)
