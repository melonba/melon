import serial
import time
from datetime import datetime
import json
from flask import Flask, jsonify
import csv
import AI_rasp as ai
import os
    
def test():
    path = os.path.dirname(os.path.abspath(__file__))
    
    with open(os.path.join(path, "red.log"), "w") as f:
        pass
    
    A = ai.BpMonitoringSystemByAi()
    read_c = A.load_collection_data(os.path.join(path, "userInfo.csv"))
    print(type(read_c))

    f = open(os.path.join(path, "userInfo.csv"), 'r')
    rdr = csv.reader(f)
    usernameValue = ''
    for line in rdr:
        usernameValue = line[1]
    f.close()

    id = usernameValue
    print("ID: ", id)
    
    My_data={}
    My_red=[]
    My_spo2=[]


    Measure_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    port = '/dev/ttyUSB0'
    brate = 115200
    cmd = 'temp'

    seri = serial.Serial(port, baudrate = brate, timeout = None)
    print(seri.name)
    seri.write(cmd.encode())

    a = 0
    b = 0
    while 80 > a:
        if seri.in_waiting !=0:
            content = seri.readline()
            print(content[:-2].decode())
            x = content[:-2].decode()
            if 'red' in x:
                x=x.replace("red","")
                with open(os.path.join(path, "red.log"), "a") as f:
                    f.write("{0}\n".format(int(x)))
                My_red.append(int(x))
            if 'spo2' in x:
                x=x.replace("spo2","")
                My_spo2.append(int(x))
                a=a+1
                
    a = []
    with open(os.path.join(path, "red.log"), "r") as f:
        for i, ppg in enumerate(f):
            a.append(int(ppg))
    avgsum = 0
    for ppg_el in a:
        avgsum = ppg_el + avgsum
    avg = avgsum/(i+1)

    for i in range(len(a)):
        a[i] = a[i] - int(avg)

    with open(os.path.join(path, 'ppg.csv'), 'w', newline='') as f:
        f.write(",PPG\n")

        for i, value in enumerate(a):
            f.write(str(i) + ",")
            f.write(str(value)+"\n")
    print("csv dhks")

    with open(os.path.join(path, "red.log"), 'w') as f:
        for i in range(len(a)):
            f.write("{0}\n".format(a[i]))

    # AI part
    path5 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "userInfo.csv")
    path1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ppg.csv")
    path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rp_text.csv")
    print(path1 + "|"+ path2)

    A.rp_preprocess(path1, path5)
    BP_D, BP_S = A.predict(path2)
    
    My_bp = []
    My_bp.append(BP_S)
    My_bp.append(BP_D)

    RED = []
    with open(os.path.join(path, "red.log"), "r") as f:
        for r in f:
            r = r.strip('\n')
            RED.append(int(r))
   #--------------------------------server-------------------------------
    My_data={
            'username':id,
            'datatime':Measure_time,
            'spo2_data':{    
                'spo2':My_spo2
                    },
            'bp_data':{
                'bp':My_bp
                },
            'ppg_data':{
            'ppg':My_red
            },
            'avg_spo2':round(sum(My_spo2)/len(My_spo2),2),
            'min_spo2':min(My_spo2),
            'max_spo2':max(My_spo2)
            }

    print(id+Measure_time)
    #return My_data
    with open('/home/pi/spo2_project/max30102-tutorial-raspberrypi/templates/spo2.json', 'w', encoding='utf-8') as make_json:
        json.dump(My_data, make_json, indent="\t")
    seri.close()
