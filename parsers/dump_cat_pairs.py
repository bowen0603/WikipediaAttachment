__author__ = 'bobo'

from mw.xml_dump import Iterator
from mw.xml_dump import functions
import mwparserfromhell as mwp

###############################################################
## Code Description
##
## this code parse articles of namespace 14 to get category page info
## for each page, the categories at the bottom are its super categories.
##
###############################################################
## Category relation
## schema: {"cate": cate, "super_cate": super_cate, "cate_pid": page.id}
##
###############################################################
## Input files: <input_file> <output_file>
## dump meta current page file; output file name with file type; bot list file
##

def generate_category_relation(input=None, output=None):
    fout = open(output, 'w')
    dump = Iterator.from_file(functions.open_file(input))

    for page in dump:

        # ignore redirected pages for both article and talk pages
        if page.redirect:
            continue
        # only parse category page
        if page.namespace != 14:
            continue

        # only one revision on the current page
        for rev in page:
            try:
                wikicode = mwp.parse(rev.text)
            except:
                print(page.id, page.title, page.namespace)
                continue

            # parse the article page to extract category info of the article
            cate = page.title.lower()[len("category:"):]
            for link in wikicode.filter_wikilinks():
                if link.title.startswith('Category:'):
                    super_cate = link.title.lower().replace('category:', "")
                    # categories.append(cate)
                    record = {"cate": cate, "super_cate": super_cate, "cate_pid": page.id}
                    from json import dumps
                    print(dumps(record), file=fout)


def main(argv=None):
    if len(argv) != 3:
        print("usage: <input_file> <output_file>")
        return

    generate_category_relation(argv[1], argv[2])

if __name__ == '__main__':
    from sys import argv
    main(argv)
