# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 16:30:31 2016

@author: alyshareinard
"""
import os
import glob
import matplotlib.pyplot as plt
from datetime import datetime
import sys

def read_rtsw_ace():
    if os.sep=="/":
        osdir=os.sep+os.path.join("Users", "alyshareinard")
    else:
        osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard.SWPC")

    rootdir=os.path.join(osdir, "Dropbox", "Work", "data", "DSCOVR")+os.sep
    
    acelist=glob.glob(os.path.join(rootdir, '*mag_1m.txt'))
    date=[]
    year=[]
    month=[]
    day=[]
    time=[]
    s=[]
    bx=[]
    by=[]
    bz=[]
    bt=[]
    lat=[]
    lon=[]
    for acefile in acelist:
        
        with open(acefile, "r") as f:
            ace_data=f.readlines()
        for line in ace_data:
#            year.append(line[0:4])
#            month.append(line[5:7])
#            day.append(line[8:10])
#            time.append(line[12:16])
            
#            print("year", line[0:4])
            line=str(line)
            print("line", line)
            if line[0]!=":" and line[0]!="#":
                year=int(line[0:4])
                month=int(line[5:7])
                day=int(line[8:10])
                hour=int(line[12:14])
                minute=int(line[14:16])
                time=int(line[12:16])
                print(year, month, day, hour, minute)
                date.append(datetime(year, month, day, hour, minute))
            
                s.append(line[32:38])
                bx.append(line[39:46])
                by.append(line[47:54])
                bz.append(line[55:62])
                bt.append(line[63:70])
                lat.append(line[71:78])
                lon.append(line[77:85])  
#            except Exception as e: 
#                print(str(e))
          

#    print("year", year[700:720])
#    print("month", month[700:720])
#    print("day", day[700:720])
#    print("time", time[700:720])
    print("s", s[700:720])
    print("bx", bx[700:720])
    print("by", by[700:720])
    print("bz", bz[700:720])
    print("bt", bt[700:720])
    print("lat", lat[700:720])
    print("lon", lon[700:720])
    print("date", date[700:720])

read_rtsw_ace()
