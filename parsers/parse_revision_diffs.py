__author__ = 'bobo'

###############################################################
## Code Description
##
## this code parses the content of parsed file from Aaron's code to extract all the
## revision records without the text info.
##
## for now, this code is not used yet, as we don't need the revision contents
##
###############################################################

def parse_file(input, output):
    with open(output, 'w') as fout:
        for line in open(input, 'r'):
            from json import loads
            raw_record = loads(line)

            if raw_record['contributor']['id'] == -1:
                continue

            from time import mktime, strptime
            pattern = '%Y-%m-%dT%H:%M:%SZ'
            epoch = int(mktime(strptime(raw_record['timestamp'], pattern)))

            # diff content is needed later?
            record = {"rev_id": raw_record['id'], "rev_page": raw_record['page']['id'],
                      "rev_user": raw_record['contributor']['id'],
                      "rev_user_text": raw_record['contributor']['user_text'], "rev_timestamp": epoch}

            from json import dumps
            print(dumps(record), file=fout)
            # fout.write(dumps(record) + '\n')


def main(argv=None):
    # give the input and output filenames
    if len(argv) != 3:
        print("usage: <input_file> <output_file>")
        return

    parse_file(input=argv[1], output=argv[2])

if __name__ == '__main__':
    from sys import argv
    main(argv)
