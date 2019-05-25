__author__ = 'bobo'

def parse_file(input, output):
    with open(output, 'w') as fout:
        for line in open(input, 'r'):
            fout.write(line.replace('\n', '') + '*\n')


def main(argv=None):
    # give the input and output filenames
    if len(argv) != 3:
        print("usage: <input_file> <output_file>")
        return

    parse_file(input=argv[1], output=argv[2])

if __name__ == '__main__':
    from sys import argv
    main(argv)