__author__ = 'bobo'

from mw.xml_dump import Iterator
from mw.xml_dump import functions

###############################################################
## Code Description
##
## the code take in one meta dump page current file as input for parsing.
## it parses all the revision record in the file ignoring those edited by bots, and anonymous editors.
## it parses handles all the namespaces, but will not extract the particular editing texts.
##
###############################################################
## Revision Records
## for each revision record, mark down all its importance information. timestamp is converted to epoch
## schema: {"rev_id": rev.id, "rev_page_id": page.id, "rev_page_title": page.title,
##                      "rev_user_id": rev.contributor.id, "rev_user_text": rev.contributor.user_text,
##                      "ns": page.namespace, "rev_timestamp": epoch}
##
###############################################################
## Input files: <input_file> <output_file> <bot_file>
## dump meta current page file; output file name with file type; bot list file
##
## Choose whether to store the categories or wikiprojects of an article in a list,
## or single record per line by setting LIST_FORMAT
##

def load_bots(bot_file):
    bot_list = []
    for bot in open(bot_file, 'r'):
        bot_list.append(bot)
    return bot_list

def parse_file(input=None, output=None, bot_file=None):

    bot_list = load_bots(bot_file)

    fout = open(output, 'w')
    dump = Iterator.from_file(functions.open_file(input))

    for page in dump:
        # ignore old version pages that were redirected
        if page.redirect:
            continue

        for rev in page:

            user_text = rev.contributor.user_text
            from IPy import IP
            try:
                IP(user_text)
                continue
            except:
                if user_text in bot_list:
                    continue

            from time import mktime, strptime
            pattern = '%Y%m%d%H%M%S'
            epoch = int(mktime(strptime(str(rev.timestamp), pattern)))

            record = {"rev_id": rev.id, "rev_page_id": page.id, "rev_page_title": page.title,
                      "rev_user_id": rev.contributor.id, "rev_user_text": rev.contributor.user_text,
                      "ns": page.namespace, "rev_timestamp": epoch}

            from json import dumps
            print(dumps(record), file=fout)


def main(argv=None):
    # give the input and output filenames, wp and cat data will be parsed into different folders
    if len(argv) != 4:
        print("usage: <input_file> <output_file> <bot_file>")
        return

    parse_file(input=argv[1], output=argv[2], bot_file=argv[3])

if __name__ == '__main__':
    from sys import argv
    main(argv)

