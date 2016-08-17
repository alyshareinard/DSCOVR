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

def scatter_plot(ace, dscovr):

    #choose which data product we want to plot
    ace_product=ace.lon
    dscovr_product=dscovr.lon
    #align data
    ace_data=[]
    dscovr_data=[]
    dscovr_index=0
    for index in range(len(ace.date)):
#        print(index)
        while dscovr.date[dscovr_index]<ace.date[index]:
            dscovr_index+=1
            print("skipping dscovr, no ace")
        if dscovr.date[dscovr_index]==ace.date[index]:
#            print("got one!")
            if ace_product[index]>-500 and dscovr_product[index]>-500:
                val=ace_product[index]+120
                if val>400: val=val-360
#                ace_data.append(ace_product[index])
                ace_data.append(val)
                dscovr_data.append(dscovr_product[dscovr_index])
            dscovr_index+=1
        else:
            print("skipping ace, no dscovr")
            
    #plot
    plt.plot(ace_data, dscovr_data, 'b.')
    plt.title("ACE+120, phi/lon from August 10-16, 2016")
    plt.xlabel("ACE data")
    plt.ylabel("DSCOVR data")
    plt.plot([0,400], [0,400])
    plt.show()        
        

def plot_bt_lat_lon(ace, dscovr):
    plt.subplot(3,1,1) 
    plt.plot(ace.date, ace.bt, 'r.')
    plt.plot(dscovr.date, dscovr.bt, 'b.')
    plt.ylim(0, 10)
    plt.ylabel("bt")
    plt.xticks([])  
    
    plt.subplot(3,1,2) 
    plt.plot(ace.date, ace.lat, 'r.')
    plt.plot(dscovr.date, dscovr.lat, 'b.')
    plt.ylim(-120, 120)
    plt.ylabel("lat")
    plt.xticks([])  
    
    ace_lon=[x+120 for x in ace.lon]
    for index in range(len(ace_lon)):
        if ace_lon[index]>400:
            ace_lon[index]=ace_lon[index]-360
    
    plt.subplot(3,1,3) 
    
    plt.plot(dscovr.date, dscovr.lon, 'b.')
    plt.plot(ace.date, ace_lon, 'r.')
    plt.ylim(-30, 420)
    plt.ylabel("lon")
    
#    plt.xticks([])  
#    
#    plt.subplot(7,1,7) 
#    plt.plot(ace.date, ace.s, '.')
#    plt.ylim(0, 10)
#    plt.ylabel("s")
#    plt.xticks([])  
#    plt.show()
    
def plot_bx_by_bz(ace, dscovr):
    plt.subplot(3,1,1) 
    plt.plot(ace.date, ace.bx, '.')
    plt.plot(dscovr.date, dscovr.bx, '.')
    plt.ylim(0, 20)
    plt.ylabel("bx")
    plt.xticks([]) 
    
    plt.subplot(3,1,2) 
    plt.plot(ace.date, ace.by, '.')
    plt.plot(dscovr.date, dscovr.by, '.')
    plt.ylim(0, 20)
    plt.ylabel("by")
    plt.xticks([])   
    
    plt.subplot(3,1,3) 
    plt.plot(ace.date, ace.bz, '.')
    plt.plot(dscovr.date, dscovr.bz, '.')
    plt.ylim(0, 20)
    plt.ylabel("bz")
    plt.xticks([])  
    

class ace_class:
    
    def __init__(self):
        if os.sep=="/":
            osdir=os.sep+os.path.join("Users", "alyshareinard")
        else:
            osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard.SWPC")
    
        rootdir=os.path.join(osdir, "Dropbox", "Work", "data", "DSCOVR")+os.sep
        
        acelist=glob.glob(os.path.join(rootdir, '*mag_1m.txt'))
        self.date=[]
        self.s=[]
        self.bx=[]
        self.by=[]
        self.bz=[]
        self.bt=[]
        self.lat=[]
        self.lon=[]
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
                    self.date.append(datetime(year, month, day, hour, minute))
                
                    self.s.append(int(line[6]))
                    self.bx.append(float(line[7]))
                    self.by.append(float(line[8]))
                    self.bz.append(float(line[9]))
                    self.bt.append(float(line[10]))
                    self.lat.append(float(line[11]))
                    self.lon.append(float(line[12]))
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


    
    
class dscovr_class:
    def __init__(self):
        if os.sep=="/":
            osdir=os.sep+os.path.join("Users", "alyshareinard")
        else:
            osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard.SWPC")
    
        rootdir=os.path.join(osdir, "Dropbox", "Work", "data", "DSCOVR")+os.sep
        
        dscovr_file=os.path.join(rootdir, 'rtsw_plot_data.txt')
        self.date=[]
        self.bx=[]
        self.by=[]
        self.bz=[]
        self.bt=[]
        self.lat=[]
        self.lon=[]
            
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
                self.date.append(datetime(year, month, day, hour, minute, sec))
    #            print(date)
                self.bt.append(float(line[2]))
                self.bx.append(float(line[3]))
                self.by.append(float(line[4]))
                self.bz.append(float(line[5]))
                self.lon.append(float(line[6]))
                self.lat.append(float(line[7]))



dscovr=dscovr_class()
ace=ace_class()

#plot_bx_by_bz(ace, dscovr)
#plot_bt_lat_lon(ace, dscovr)
scatter_plot(ace, dscovr)






