# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 16:25:58 2016

@author: alysha.reinard
"""
import csv
import os
import matplotlib.pyplot as plt
from datetime import datetime

def read_fc(filename):
    
    if os.sep=="/":
        osdir=os.sep+os.path.join("Users", "alyshareinard")
    else:
        osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard.SWPC")
    rootdir=os.path.join(osdir, "Dropbox", "Work", "data", "DSCOVR")+os.sep
    print("fulldir", rootdir+filename)

    timestamp=[]
    cadence=[]
    speed=[]
    temperature=[]
    density=[]
    sample_size=[]
    data_flag=[]
    processing_flag=[]
    range_flag=[]
    sample_count_flag=[]
    overall_quality=[]

    with open(rootdir+filename, 'r') as csvfile:
        data=csv.reader(csvfile, delimiter=',', quotechar="|")
        header=data.__next__()
        print("header", header)
        for line in data:
            date=line[0]
            date=date.replace(':', '-').replace(' ', '-').split('-')
            dateints=[int(round(float(x))) for x in date]
            timestamp.append(datetime(dateints[0], dateints[1], dateints[2], dateints[3], dateints[4], dateints[5]))
            cadence.append(int(line[1]))
            speed.append(float(line[2]))
            temperature.append(float(line[3]))
            density.append(float(line[4]))
            sample_size.append(int(line[5]))
            data_flag.append(int(line[6]))
            processing_flag.append(int(line[7]))
            range_flag.append(int(line[8]))
            sample_count_flag.append(int(line[9]))
            overall_quality.append(int(line[10]))
            
#    print(overall_quality)
    plt.plot(timestamp, temperature)

#    start=[]
#    peak=[]
#    end=[]
#    left=[]
#    right=[]
#    width=[]
#
#    for line in data:
#        vals=line.split()
#        print(vals)
        
        
#read_fc("fc_out.csv")
read_fc("fc_mls_hack2_062216_101716_L2.csv")