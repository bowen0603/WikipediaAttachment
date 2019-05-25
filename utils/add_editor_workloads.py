__author__ = 'bobo'

SAMPLE_SIZE = 50

def add_user_wp_workloads(input, output):
    wps_all = []
    wps_sample = []

    for line in open(input, 'r'):
        wps_all.append(line.replace('\n', ''))


    with open(output, 'w') as fout:
        pre_user = ""
        for line in open(input, 'r'):
            # print line.split(",")
            items = line.split(",")
            # user, wp, ts = line.split(",")
            if pre_user != items[0]:
                rank = 0
                pre_user = items[0]
                fout.write(items[0] + "\t" + items[1] + "\t" + str(rank) + "\n")
            else:
                fout.write(items[0] + "\t" + items[1] + "\t" + str(rank) + "\n")
                #fout.write(str(user) + "," + wp + "," + str(rank) + "\n")

            rank += 1


def main(argv=None):
    # give the input and output filenames
    if len(argv) != 3:
        print("usage: <input_file> <output_file>")
        return

    add_user_wp_workloads(input=argv[1], output=argv[2])


if __name__ == '__main__':
    from sys import argv
    main(argv)