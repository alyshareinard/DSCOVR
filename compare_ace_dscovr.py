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
#            print("line", line)
            if line[0]!=":" and line[0]!="#":
                line=line.split()
                
                year=int(line[0])
                month=int(line[1])
                day=int(line[2])
                hhmm=line[3]
                hour=int(hhmm[0:2])
                minute=int(hhmm[2:4])
                date.append(datetime(year, month, day, hour, minute))
            
                s.append(int(line[6]))
                bx.append(float(line[7]))
                by.append(float(line[8]))
                bz.append(float(line[9]))
                bt.append(float(line[10]))
                lat.append(float(line[11]))
                lon.append(float(line[12]))
#            except Exception as e: 
#                print(str(e))
          

#    print("year", year[700:720])
#    print("month", month[700:720])
#    print("day", day[700:720])
#    print("time", time[700:720])
#    print("s", s[700:720])
#    print("bx", bx[700:720])
#    print("by", by[700:720])
#    print("bz", bz[700:720])
#    print("bt", bt[700:720])
#    print("lat", lat[700:720])
#    print("lon", lon[700:720])
#    print("date", date[700:720])

#    fig=plt.figure()
    
#    bx=fig.add_subplot
    plt.subplot(7,1,1) 
    plt.plot(date, bx, 'o-')
    plt.ylim(0, 20)
    plt.ylabel("bx")
    plt.xticks([]) 
    
    plt.subplot(7,1,2) 
    plt.plot(date, by, 'o-')
    plt.ylim(0, 20)
    plt.ylabel("by")
    plt.xticks([])   

    plt.subplot(7,1,3) 
    plt.plot(date, bz, 'o-')
    plt.ylim(0, 20)
    plt.ylabel("bz")
    plt.xticks([])  
    
    plt.subplot(7,1,4) 
    plt.plot(date, bt, 'o-')
    plt.ylim(0, 20)
    plt.ylabel("bt")
    plt.xticks([])  
    
    plt.subplot(7,1,5) 
    plt.plot(date, lat, 'o-')
    plt.ylim(-90, 90)
    plt.ylabel("lat")
    plt.xticks([])  
    
    plt.subplot(7,1,6) 
    plt.plot(date, lon, 'o-')
    plt.ylim(0, 360)
    plt.ylabel("lon")
    plt.xticks([])  
    
    plt.subplot(7,1,7) 
    plt.plot(date, s, 'o-')
    plt.ylim(0, 10)
    plt.ylabel("s")
    plt.xticks([])  
    plt.show()
    
    
def read_rtsw_dscovr():
    if os.sep=="/":
        osdir=os.sep+os.path.join("Users", "alyshareinard")
    else:
        osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard.SWPC")

    rootdir=os.path.join(osdir, "Dropbox", "Work", "data", "DSCOVR")+os.sep
    
    dscovr_file=os.path.join(rootdir, 'rtsw_plot_data.txt')
    date=[]
    bx=[]
    by=[]
    bz=[]
    bt=[]
    lat=[]
    lon=[]
        
    with open(dscovr_file, "r") as f:
        dscovr_data=f.readlines()
    for line in dscovr_data:
        if line[0]!="T":
            line=line.split()
#            print(line)
            ymd=line[0].split("-")
#            print(ymd)
            year=int(ymd[0])
            month=int(ymd[1])
            day=int(ymd[2])
            hms=line[1].split(":")
            hour=int(hms[0])
            minute=int(hms[1])
            sec=int(round(float(hms[2])))
#            print(year, month, day, hour, minute, sec)
            date.append(datetime(year, month, day, hour, minute, sec))
#            print(date)
            bt.append(line[2])
            bx.append(line[3])
            by.append(line[4])
            bz.append(line[5])
            lat.append(line[6])
            lon.append(line[7])


read_rtsw_ace()

#read_rtsw_dscovr()
