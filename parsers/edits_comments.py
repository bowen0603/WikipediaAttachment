__author__ = 'bobo'

def parser(input):
    # with open(output, 'w') as fout:
    header = True
    tot_comment = ""
    for line in open(input, 'r'):
        if header:
            header = False
            continue

        # id, timestamp, comment = map(str, line.split(","))
        tot_comment += line.rstrip() + " "

    print(tot_comment)

def main(argv=None):
    # give the input and output filenames
    if len(argv) != 2:
        print("usage: <input_file>")
        return

    parser(input=argv[1])


if __name__ == '__main__':
    from sys import argv
    main(argv)