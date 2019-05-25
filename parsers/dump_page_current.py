__author__ = 'bobo'

from mw.xml_dump import Iterator
from mw.xml_dump import functions
import mwparserfromhell as mwp

###############################################################
## Code Description
##
## the code take in one meta dump page current file as input for parsing.
## for an article, as category info is in article (ns=0), and wikiproject info is in talk page (ns=1),
## the code generates the output into these two directories for the two types of info - wp_dir and cat_dir
## with the same output file name for each input.
##
###############################################################
## 1. Category Info
## use the categories listed at the bottom of each article page (ns=0),
## filtered by wikilinks tags.
## schema: {"pageId": page.id, "title": title, "categories": categories}
##
## 2. WikiProject Info
## use the wikiprojects the article belongs to listed in the article talk page (ns=1)
## filtered by template tags.
## schema: {"pageId": page.id, "title": title, "wikiproject": wikiproject, "class": cls, "importance": importance}
##
## All texts are stored in LOWER CASES.
##
###############################################################
## Input files: <input_file> <output_file> <wp_dir> <cat_dir>
## dump meta current page file; output file name with file type; wp directory; category directory
##
## Choose whether to store the categories or wikiprojects of an article in a list,
## or single record per line by setting LIST_FORMAT
##

# config
LIST_FORMAT = False
FILE_TYPE = '.json'

def parse_file(input=None, output=None, wp_dir=None, cat_dir=None):

    wp_output = wp_dir + output.replace(FILE_TYPE, '') + '_wikiproject' + FILE_TYPE
    cat_output = cat_dir + output.replace(FILE_TYPE, '') + '_category' + FILE_TYPE
    wp_fout = open(wp_output, 'w')
    cat_fout = open(cat_output, 'w')

    dump = Iterator.from_file(functions.open_file(input))

    for page in dump:
        # print(page.title, page.namespace)
        # ignore redirected pages for both article and talk pages
        if page.redirect:
            continue
        if page.namespace != 0 and page.namespace != 1:
            continue

        # only one revision on the current page
        for rev in page:
            # catch rare parsing errors
            try:
                wikicode = mwp.parse(rev.text)
            except:
                print(page.id, page.title, page.namespace)
                continue

            # parse the article page to extract category info of the article
            if page.namespace == 0:
                categories = []
                title = page.title.lower()
                for link in wikicode.filter_wikilinks():
                    if link.title.startswith('Category:'):
                        cate = link.title.lower().replace('category:', "")
                        categories.append(cate)

                        if not LIST_FORMAT:
                            record = {"pageId": page.id, "title": title, "category": cate}
                            from json import dumps
                            print(dumps(record), file=cat_fout)

                if LIST_FORMAT:
                    record = {"pageId": page.id, "title": title, "categories": categories}
                    from json import dumps
                    print(dumps(record), file=cat_fout)

            # parse the talk page to extract wikiproject info of the article
            if page.namespace == 1:
                title = page.title.lower().replace("talk:", "")
                cls = importance = "None"
                wikiprojects = []

                for template in wikicode.filter_templates():
                    if template.name == 'WikiProjectBannerShell':
                        continue

                    if template.name.lower().startswith('wikiproject'):
                        from re import search
                        wikiproject = template.name.lower().replace("wikiproject", "").strip()
                        wikiprojects.append(wikiproject)
                        template = str(template).replace("}", "|").replace(" ", "").replace("\n", "")

                        try:
                            cls = search(r'\|class=([a-z-A-Z]+)\|', template).group(1)
                            importance = search(r'\|importance=([a-z-A-Z]+)\|', template).group(1)
                        except AttributeError:
                            pass

                        if not LIST_FORMAT:
                            record = {"pageId": page.id, "title": title, "wikiproject": wikiproject, "class": cls.lower(), "importance": importance.lower()}
                            from json import dumps
                            print(dumps(record), file=wp_fout)

                if LIST_FORMAT:
                    record = {"pageId": page.id, "title": title, "wikiprojects": wikiprojects, "class": cls.lower(), "importance": importance.lower()}
                    from json import dumps
                    print(dumps(record), file=wp_fout)


def create_directory(dir_name):
    from os import path, makedirs
    if not path.exists(dir_name):
        makedirs(dir_name)


def main(argv=None):
    # give the input and output filenames, wp and cat data will be parsed into different folders
    if len(argv) != 5:
        print("usage: <input_file> <output_file> <wp_dir> <cat_dir>")
        return

    create_directory(argv[3])
    create_directory(argv[4])

    parse_file(input=argv[1], output=argv[2], wp_dir=argv[3], cat_dir=argv[4])

if __name__ == '__main__':
    from sys import argv
    main(argv)

