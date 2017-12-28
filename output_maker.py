#!/usr/bin/python

import random
import json
import ast

number_of_sockets = 0
number_of_cores = 0


def construct_pqos_output():
    global number_of_cores, number_of_sockets
    configuration_info = json.load(open("config.json"))
    number_of_sockets = len(configuration_info["sockets"].keys())
    total_cores_list = []
    for socket_id in range(number_of_sockets):
        cores_list = configuration_info["sockets"][str(socket_id)]
        cores_list = ast.literal_eval(cores_list)
        for x in cores_list:
            total_cores_list.append(x)
            number_of_cores = number_of_cores + len(cores_list)
            with open("sample1_cmt_output.txt", "wb") as fwrite:
                for i in range(100):
                    fwrite.write("CORE   IPC     MISSES   LLC[KB]    MBL[MB/s]   MBR[MB/s]\n")
                    for core in total_cores_list:
                        llc = random.randint(1, 9)
                        ipc = random.randrange(20, 320, 1)
                        mbl = random.randint(1, 9)
                        if core < 10:
                            fwrite.write(
                                "%s     %.2f       0k     %.1f        %.1f        0.0\n" % (core,
                                                                                            float(ipc)/100.0,
                                                                                            float(llc*1024),
                                                                                            mbl*1000.0)
                            )
                        else:
                            fwrite.write(
                                "%s    %.2f       0k     %.1f        %.1f        0.0\n" % (core,
                                                                                           float(ipc)/100.0,
                                                                                           float(llc*1024),
                                                                                           mbl*1000.0)
                            )


if __name__ == "__main__":
    construct_pqos_output()
