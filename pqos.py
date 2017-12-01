#!/usr/bin/env python
import time
import sys
import os
import signal
import cPickle as pickle
import os.path

sockets_list = [0,1]
number_of_cos = 8
cos = []
cores = []


def signal_handler(signal, frame):
    sys.exit(0)


def print_metrics():
    with open("file.txt", "r") as fread:
        t1 = time.time()
        count = 1;
        while True:
            waiting = 1
            for line in fread:
                if count % 3 != 0:
                    sys.stdout.write(line)
                    count = count + 1
                else:
                    sys.stdout.write(line)
                    count = count + 1
                    break
            else:
                fread.seek(0)
                waiting = 0
            if (waiting):
                t2 = time.time()
                if t2-t1 < 1.0:
                    time.sleep(1.0 - (t2-t1))
                    t1 = time.time()
                    sys.stdout.write("\033[F")
                    sys.stdout.write("\033[F")

                    #sys.stdout.write("\033[F")
                    #sys.stdout.write("\033[F")
                    #sys.stdout.write("\033[F")
                    #sys.stdout.write("\033[F")
                    #sys.stdout.write("\033[F")
                    sys.stdout.write("\033[F")
                    sys.stdout.write("\033[K")


def print_cur_config():
    global cos
    for i in range(0,8):
        cos.append("0xffff")
    for socket in sockets_list:
        print("L3CA COS definitions for Socket %d:" %socket)
        for i in range(0,number_of_cos):
            print("L3CA COS%d => MASK %s" %(i,cos[i]))


def reset_cos():
    global cos
    for i in range(0,8):
        cos[i] = "0xfffff"
    pickle.dump(cos, open("cos_mask.p", "wb"))
    print("NOTE:  Mixed use of MSR and kernel interfaces to manage");
    print("       CAT or CMT & MBM may lead to unexpected behavior.")


def change_cos():
    global cores
    new_config = sys.argv[2].strip('"');
    print(new_config)
    splitted = new_config.split(";")
    splitted = splitted[:-1]
    print(splitted)
    for config in splitted:
        splitted_config = config.strip('llc')
        print(splitted_config)
        cores = splitted_config.strip(":").split("=")[0]
        list_of_cores = splitted_config.strip(":").split("=")[1]
        print(cores, list_of_cores)


def change_mask():

    global cos
    new_config = sys.argv[2].strip('"');
    splitted = new_config.split(";")
    splitted = splitted[:-1]
    for config in splitted:
        splitted_config = config.strip('llc')
        cos_number = splitted_config.strip(":").split("=")[0]
        mask = splitted_config.strip(":").split("=")[1]
        cos[int(cos_number)] = mask
    pickle.dump(cos, open("cos_mask.p", "wb"))


def main():
    global cos, cores
    if os.path.isfile("cos_mask.p"):
        cos = pickle.load(open("cos_mask.p", "rb"))
    else:
        for i in range(0,8):
            cos.append("0xffff")

    if os.path.isfile("cos_core.p"):
        cores = pickle.load(open("cos_core.p", "rb"))
    else:
        for i in range(0,22):
            cores.append(0)

    signal.signal(signal.SIGINT, signal_handler)

    if (sys.argv[1] == "-r"):
        print_metrics()
    elif (sys.argv[1] == "-sv"):
        print_cur_config()
    elif (sys.argv[1] == "-R"):
        reset_cos()
    elif (sys.argv[1] == "-a"):
        change_cos()
    elif (sys.argv[1] == "-e"):
        change_mask()



if __name__ == "__main__":
 main()