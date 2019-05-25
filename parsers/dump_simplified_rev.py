__author__ = 'bobo'

from mw.xml_dump import Iterator
from mw.xml_dump import functions

###############################################################
## Code Description
##
## the code take in one stub meta dump file as input for parsing.
## it parses all the revision record in the file of all users.
## it parses handles all the namespaces, but will not extract the particular editing texts.
##
###############################################################
## Revision Records
## for each revision record, mark down all its importance information. timestamp is converted to epoch
## schema: {"rev_id": rev.id, "rev_page_id": page.id, "rev_page_title": page.title,
##                      "rev_user_id": rev.contributor.id, "rev_user_text": rev.contributor.user_text,
##                      "ns": page.namespace, "rev_comment": rev.comment, "rev_timestamp": epoch}
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
            print(page.title)
            # print(page.redirect_title)
            continue

        for rev in page:

            from time import mktime, strptime
            pattern = '%Y-%m-%d%HT%M%SZ'
            pattern = '%Y%m%d%H%M%S'
            epoch = int(mktime(strptime(str(rev.timestamp), pattern)))

            record = {"rev_id": rev.id, "rev_page_id": page.id, "rev_page_title": page.title,
                      "rev_user_id": rev.contributor.id, "rev_user_text": rev.contributor.user_text,
                      "ns": page.namespace, "rev_comment": rev.comment, "rev_timestamp": epoch}

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
