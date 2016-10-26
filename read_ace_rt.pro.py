# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 15:09:48 2016

@author: alyshareinard
"""

import os
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

def read_ace_rt():
    
    
    if os.sep=="/":
        osdir=os.path.join("/Users", "alyshareinard")
    else:
        osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard.SWPC")

    date=[]
    density=[]
    speed=[]
    temp=[]
    for year in range(1998, 2015):
        rootdir=os.path.join(osdir, "Dropbox", "Work", "data", "ACE", "real-time", str(year))+os.sep
        print("fulldir", rootdir)

        try:
            files=os.listdir(rootdir)
        except:
            print("Nothing found")
            files=[]
#        print(files)
        for file in files:
            if "swepam_1m.txt" in file:
                with open(rootdir+file, "r") as data:
                    header=[]
                    for next in range(18):
                        header.append(data.__next__())
#                    print("header", header)
                    for line in data:
                        line=line.split()
                        date.append(datetime(int(line[0]), int(line[1]), int(line[2]),int(line[3][0:2]), int(line[3][2:4])))
                        density.append(float(line[7]))
                        speed.append(float(line[8]))
                        temp.append(float(line[9]))
#                        pass



    pos_speed=[x for x in speed if x>0]
    pos_density=[x for x in density if x>0]
    pos_temp=[x for x in temp if x>0]
    
    print("speed", min(pos_speed), max(speed), np.percentile(pos_speed, 0.1), np.percentile(pos_speed, 99.9))
    print("density", min(pos_density), max(density), np.percentile(pos_density, 0.1), np.percentile(pos_density, 99.9))
    print("temperature", min(pos_temp), max(temp), np.percentile(pos_temp, 0.1), np.percentile(pos_temp, 99.9))

    n, bins, patches = plt.hist(pos_speed)#, 50, normed=1, histtype='stepfilled')
    plt.setp(patches, 'facecolor', 'g', 'alpha', 0.75)

#    plt.plot(date, speed)
#    plt.ylim(ymin=0)
    plt.show()
#                print("datafile", ace_data)

read_ace_rt()
