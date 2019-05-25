__author__ = 'bobo'

SAMPLE_SIZE = 50

def random_sample(input, output):
    wps_all = []
    wps_sample = []

    for line in open(input, 'r'):
        wps_all.append(line.replace('\n', ''))

    with open(output, 'w') as fout:
        cnt = 0
        while cnt < SAMPLE_SIZE:

            from random import randint
            idx = randint(0, len(wps_all))
            elem = wps_all[idx]
            print(idx, elem)
            if elem not in wps_sample:
                wps_sample.append(elem)
                fout.write(elem + "\n")
                cnt += 1


def main(argv=None):
    # give the input and output filenames
    if len(argv) != 3:
        print("usage: <input_file> <output_file>")
        return

    random_sample(input=argv[1], output=argv[2])


if __name__ == '__main__':
    from sys import argv
    main(argv)