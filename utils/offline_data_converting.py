from __future__ import print_function
__author__ = 'bobo'

MONTH = 3
TIME_INTERVAL = 3600 * 24 * 30 * MONTH
MIN_INTERVAL_NUM = 3


def create_time_intervals(input, output):

    with open(output, 'w') as fout:
        print("user_id,nwikiproject,start_ts,end_ts,count", file=fout)

        header = True
        for line in open(input, 'r'):

            if header:
                header = False
                continue

            uid, wpid, stts, endts = map(int, line.split(","))

            # editors active period need to be at least MIN_INTERVAL_NUM
            if endts - stts < TIME_INTERVAL * MIN_INTERVAL_NUM:
                continue

            curts = stts
            cnt = 1
            while curts + TIME_INTERVAL < endts:

                print("{},{},{},{},{}".format(uid,
                                              wpid,
                                              curts,
                                              curts + TIME_INTERVAL,
                                              cnt), file=fout)
                curts += TIME_INTERVAL
                cnt += 1

            # include the last partial time interval
            print("{},{},{},{},{}".format(uid,
                                          wpid,
                                          curts,
                                          endts,
                                          cnt), file=fout)


def create_full_time_intervals(input, output):
    with open(output, 'w') as fout:
        print("user_id,nwikiproject,start_ts,end_ts,count", file=fout)

        header = True
        error = 0
        for line in open(input, 'r'):

            if header:
                header = False
                continue

            uid, wpid, stts, joints, endts = map(int, line.split(","))
            # TODO: add the max or min interval numbers?

            # editors active period need to be at least MIN_INTERVAL_NUM
            # TODO do not set it for now
            # if endts - stts < TIME_INTERVAL * MIN_INTERVAL_NUM:
            #     continue

            # it is possible that the editor didn't make any edits after joining the project
            if joints < stts or endts < joints:
                error += 1

            if joints > stts:
                neg_num_intervals = (joints - stts) / TIME_INTERVAL
                neg_delta_interval = (joints - stts) % TIME_INTERVAL

                # the first partial interval
                print("{},{},{},{},{}".format(uid,
                                              wpid,
                                              stts,
                                              stts + neg_delta_interval,
                                              -(neg_num_intervals+1)), file=fout)

                # the continuous time intervals before the user joined the group
                curts = stts + neg_delta_interval
                for i in range(-neg_num_intervals, 0, 1):
                    print("{},{},{},{},{}".format(uid,
                                                  wpid,
                                                  curts,
                                                  curts + TIME_INTERVAL,
                                                  i), file=fout)
                    curts += TIME_INTERVAL

            # still, to void the case where no edits are made after joining the project
            if endts > joints:
                # create the intervals after joining
                pos_num_intervals = (endts - joints) / TIME_INTERVAL
                pos_delta_interval = (endts - joints) % TIME_INTERVAL


                # the continuous time intervals after the user joined the group
                curts = stts
                for i in range(1, pos_num_intervals+1, 1):
                    print("{},{},{},{},{}".format(uid,
                                                  wpid,
                                                  curts,
                                                  curts + TIME_INTERVAL,
                                                  i), file=fout)
                    curts += TIME_INTERVAL
                # the last partial interval
                print("{},{},{},{},{}".format(uid,
                                              wpid,
                                              curts,
                                              curts + pos_delta_interval,
                                              (pos_num_intervals+1)), file=fout)
        print("{}".format(error))



def create_dv_delta(input, output):
     with open(output, 'w') as fout:
        print("user_id,nwikiproject,tcount,delta_dv", file=fout)

        header = True
        pre_wpid = -1
        pre_dv = -1
        for line in open(input, 'r'):

            if header:
                header = False
                continue

            # TODO for bond-based: int on talk count
            uid, wpid, tcount, dv = map(int, line.split(","))

            # TODO for identity-based: float on cos sim
            # uid = int(line.split(",")[0])
            # wpid = int(line.split(",")[1])
            # tcount = int(line.split(",")[2])
            # dv = float(line.split(",")[3])

            if pre_wpid != wpid:
                pre_wpid = wpid
                pre_dv = dv
                continue

            delta_dv = dv - pre_dv
            pre_dv = dv

            # need to move forward the time interval count
            if tcount != -1:
                tcount += 1
            else:
                tcount = 1

            # include the last partial time interval
            print("{},{},{},{}".format(uid,
                                       wpid,
                                       tcount,
                                       delta_dv), file=fout)


def bind_userid_nwikiproject(input, output):
    with open(output, 'w') as fout:
        print("user_wp,tcount,dlt_bonds,dlt_identity,iv_wp_tenure,iv_prior_edits,iv_avg_mbr_tenure", file=fout)

        header = True
        for line in open(input, 'r'):

            if header:
                header = False
                continue

            uid = int(line.split(",")[0])
            wpid = int(line.split(",")[1])
            tcount = int(line.split(",")[2])
            dlt_bonds = int(line.split(",")[3])
            dlt_identity = float(line.split(",")[4])
            iv_wp_tenure = int(line.split(",")[5])
            iv_prior_edits = int(line.split(",")[6])
            iv_avg_mbr_tenure = float(line.split(",")[7])

            # bind userid and nwikiproject as a new variable
            u_wp = int(str(uid) + str(wpid))

            print("{},{},{},{},{},{},{},{},{}".format(u_wp,
                                                      uid,
                                                      wpid,
                                                      tcount,
                                                      dlt_bonds,
                                                      dlt_identity,
                                                      iv_wp_tenure,
                                                      iv_prior_edits,
                                                      iv_avg_mbr_tenure), file=fout)


def main(argv=None):
    # give the input and output filenames
    if len(argv) != 3:
        print("usage: <input_file> <output_file>")
        return

    # create_time_intervals(input=argv[1], output=argv[2])
    bind_userid_nwikiproject(input=argv[1], output=argv[2])

if __name__ == '__main__':
    from sys import argv
    main(argv)