#!/usr/bin/env python
import time
import sys
import os
import signal
import cPickle as pickle
import os.path

sockets_list = [0]
number_of_cos = 8
cos = []
cores = []
number_of_cores = 4
default_cat = "0xfffff"

def signal_handler(signal, frame):
    sys.exit(0)


def print_metrics():
    os.system('clear')
    with open("file.txt", "r") as fread:
        t1 = time.time()
        count = 1;
        while True:
            waiting = 1
            for line in fread:
                if count % 9 != 0:
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
                    os.system('clear')
                    #sys.stdout.write("\033[F")
                    #sys.stdout.write("\033[K")


def print_cur_config():
    global cos, cores
    for socket in sockets_list:
        print("L3CA COS definitions for Socket %d:" %socket)
        for i in range(0,number_of_cos):
            print("L3CA COS%d => MASK %s" %(i,cos[socket][i]))
        print("Core information for socket %d:" %socket)
        for i in range(0,number_of_cores):
            print("Core %d => COS%d, RMID0" %(i,int(cores[i])))
    print("NOTE:  Mixed use of MSR and kernel interfaces to manage")
    print("CAT or CMT & MBM may lead to unexpected behavior.")
    print("INFO: Monitoring capability detected")
    print("INFO: CPUID.0x7.0: CAT supported")
    print("INFO: L3 CAT details: CDP support=0, CDP on=0, #COS=8, #ways=20, ways contention bit-mask 0xc00")
    print("INFO: L3 CAT details: cache size 9437184 bytes, 20 ways")
    print("INFO: LLC cache way size 786432 bytes")
    print("INFO: L3CA capability detected")
    print("INFO: Detected PID API (perf) support for LLC Occupancy")
    print("INFO: Detected PID API (perf) support for Instructions/Cycles")
    print("INFO: Detected PID API (perf) support for LLC Misses")


def reset_cos():
    global cos, cores
    for i in range(0, number_of_cores):
        cores[i] = 0
    pickle.dump(cores, open("cos_core.p", "wb"))
    for socket in sockets_list:
        for i in range(0, number_of_cos):
            cos[socket][i] = default_cat
    pickle.dump(cos, open("cos_mask.p", "wb"))
    print("NOTE:  Mixed use of MSR and kernel interfaces to manage");
    print("       CAT or CMT & MBM may lead to unexpected behavior.")


def change_cos():
    global cores
    new_config = sys.argv[2].strip('"');
    splitted = new_config.split(";")
    if len(splitted)> 1:
        splitted = splitted[:-1]
    for config in splitted:
        splitted_config = config.strip('llc')
        class_of_ser = splitted_config.strip(":").split("=")[0]
        list_of_cores = splitted_config.strip(":").split("=")[1]
        for core in list_of_cores.split(","):
            if len(core) == 1 and "-" not in core:
                cores[int(core)] = class_of_ser
            else:
                mini = core.split("-")[0]
                maxi = core.split("-")[1]
                for i in range(int(mini), int(maxi) + 1):
                    cores[int(i)] = class_of_ser

    pickle.dump(cores, open("cos_core.p", "wb"))


def change_mask():

    global cos
    new_config = sys.argv[2].strip('"');
    splitted = new_config.split(";")
    if len(splitted)> 1:
        splitted = splitted[:-1]
    for config in splitted:
        if '@' in config:
            splitted_config = config.strip('llc@')
            socket_id = splitted_config.split(':')[0]
            rest = splitted_config.split(':')[1]
            cos_number = rest.strip(":").split("=")[0]
            mask = rest.strip(":").split("=")[1]
            base1 = mask.lstrip("0x")
            base2 = base1.lstrip("0") or '0'
            cos[int(socket_id)][int(cos_number)] = "0x" + base2
        else:
            splitted_config = config.strip('llc')
            cos_number = splitted_config.strip(":").split("=")[0]
            mask = splitted_config.strip(":").split("=")[1]
            base1 = mask.lstrip("0x")
            base2 = base1.lstrip("0") or '0'
            cos[0][int(cos_number)] = "0x" + base2
    pickle.dump(cos, open("cos_mask.p", "wb"))


def main():
    global cos, cores
    if os.path.isfile("cos_mask.p"):
        cos = pickle.load(open("cos_mask.p", "rb"))
    else:
        cos.append([])
        cos.append([])
        for socket in sockets_list:
            for i in range(0,number_of_cos):
                cos[socket].append(default_cat)

    if os.path.isfile("cos_core.p"):
        cores = pickle.load(open("cos_core.p", "rb"))
    else:
        for i in range(0, 2 * number_of_cores):
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
