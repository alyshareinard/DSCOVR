# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 16:30:31 2016

@author: alyshareinard
"""
import os
import glob
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import numpy as np

def scatter_plot(ace, dscovr, product, start_date, end_date):

#    product="bt" #options: lon, lon+120, lat, bt, bz

    ace_date=ace.date
    ace_bx=ace.bx
    
    ace_date=[]
    ace_bx=[]
    ace_by=[]
    ace_bz=[]
    for i in range(len(ace.date)):
        if ace.date[i]>start_date and ace.date[i]<end_date:
            ace_date.append(ace.date[i])
            ace_bx.append(ace.bx[i])
            ace_by.append(ace.by[i])
            ace_bz.append(ace.bz[i])
#    print(ace_date)
    if len(ace_date)==0:
        return[0,0]
#    choose which data product we want to plot

    if product=="lon" or product=="lon+120":
        ace_product=ace.lon
        dscovr_product=dscovr.lon
        ranges=[0,400]
        if product=="lon":
            title="phi/lon from "+str(min(dscovr.date))+" to "+str(max(dscovr.date))
        elif product=="lon+120":
            title="ACE+120, phi/lon from "+str(min(dscovr.date))+" to "+str(max(dscovr.date) )
            
    elif product=="lat":
        ace_product=ace.lat
        dscovr_product=dscovr.lat
        title="theta/lat from "+str(min(dscovr.date))+" to "+str(max(dscovr.date))
        ranges=[-100,100]
    elif product=="Bt":
        ace_product=ace.bt
        dscovr_product=dscovr.bt
        title="Bt from "+str(min(dscovr.date))+" to "+str(max(dscovr.date))
        ranges=[0,10]
    elif product=="Bx":
        ace_product=ace_bx
        dscovr_product=dscovr.bx
#        title="Bx from "+str(min(dscovr.date))+" to "+str(max(dscovr.date))
        title="Bx from "+str(min(ace_date))+" to "+str(max(ace_date))
        ranges=[-8,8] 
    elif product=="By":
        ace_product=ace_by
        dscovr_product=dscovr.by
        title="By from "+str(min(dscovr.date))+" to "+str(max(dscovr.date))
        ranges=[-8,8] 
    elif product=="Bz":
        ace_product=ace_bz
        dscovr_product=dscovr.bz
        title="Bz from "+str(min(dscovr.date))+" to "+str(max(dscovr.date))
        ranges=[-8,8] 



        
    #align data
    ace_data=[]
    dscovr_data=[]
#    print("!!!!dscovr: ", len(dscovr.date), len(dscovr_product))
#    print("!!!!ace: ", len(ace_date), len(ace_product))
    dscovr_index=0
    for index in range(len(ace_date)):
#        print(index)
#        print("vals dscovr, ace", dscovr.date[dscovr_index], ace_date[index])
        while dscovr.date[dscovr_index]<ace_date[index] and dscovr_index<len(dscovr.date)-1:
            dscovr_index+=1
#            print(dscovr_index)
#            print("skipping dscovr, no ace")
        if dscovr.date[dscovr_index]==ace_date[index]:
#            print("got one!")
#            print("dscovr ace: ", dscovr_index, index)
            if ace_product[index]!=None and dscovr_product[dscovr_index]!=None and ace_product[index]>-500 and dscovr_product[dscovr_index]>-500:
                if product=="lon+120":
                    val=ace_product[index]+120
                    if val>400: val=val-360
                else: val=ace_product[index]
#                ace_data.append(ace_product[index])
                ace_data.append(val)
                dscovr_data.append(dscovr_product[dscovr_index])
            dscovr_index+=1
        else:
            pass
 #           print("skipping ace, no dscovr")
            
    #plot
    if len(dscovr_data) != len(ace_data):
        print("DSCOVR/ACE data not same length!!")
    cc=np.corrcoef(ace_data, dscovr_data)
    rms=np.sqrt(((np.array(ace_data) - np.array(dscovr_data)) ** 2).mean())
#    print(start_date, cc[0,1])
    print(start_date, cc[0,1], rms)


#    plt.plot(ace_data, dscovr_data, 'b.')
##    plt.xlim([0,10])
#    plt.title(title)
#    plt.xlabel("ACE data")
#    plt.ylabel("DSCOVR data")
#    plt.plot(ranges, ranges)
#    plt.show()   
    return [cc[0,1], rms]
#    return cc[0,1]    
        

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
    plt.plot(ace.date, ace.bx, 'b.')
    plt.plot(dscovr.date, dscovr.bx, 'r.')
    plt.ylim(-6, 6)
    plt.xlim(datetime(2016, 8, 11), datetime(2016, 8, 12))
    plt.ylabel("bx")
    plt.xticks([]) 
    plt.title("ACE (blue) and DSCOVR (red) for Aug 15, 2016")
    
    plt.subplot(3,1,2) 
    plt.plot(ace.date, ace.by, 'b.')
    plt.plot(dscovr.date, dscovr.by, 'r.')
    plt.ylim(-6, 6)
    plt.xlim(datetime(2016, 8, 11), datetime(2016, 8, 12))

    plt.ylabel("by")
    plt.xticks([])   
    
    plt.subplot(3,1,3) 
    plt.plot(ace.date, ace.bz, 'b.')
    plt.plot(dscovr.date, dscovr.bz, 'r.')

    plt.xlim(datetime(2016, 8, 11), datetime(2016, 8, 12))
    plt.ylim(-6, 6)
    plt.ylabel("bz")
#    plt.xticks([])  
    

class ace_class_web:
    
    def __init__(self):
        if os.sep=="/":
            osdir=os.sep+os.path.join("Users", "alyshareinard")
        else:
            osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard")
    
        rootdir=os.path.join(osdir, "Documents", "data", "DSCOVR")+os.sep
        
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
                    
                    
class ace_class_sql:
    
    def __init__(self, filename="ace_mag1.txt"):
        if os.sep=="/":
            osdir=os.sep+os.path.join("Users", "alyshareinard")
        else:
            osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard")
    
        rootdir=os.path.join(osdir, "Documents", "data", "DSCOVR")+os.sep
        
        acelist=glob.glob(os.path.join(rootdir, filename))
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
#                print("line", line)
                if line[0]!='P' and line[0]!=' t':
                    line=line.split()
#                    print(line)                    
                    ymd=line[0].split("-")
                    year=int(ymd[0])
                    month=int(ymd[1])
                    day=int(ymd[2])
                    hhmm=line[1].split(":")
                    hour=int(hhmm[0])
                    minute=int(hhmm[1])
                    self.date.append(datetime(year, month, day, hour, minute))
                
#                    self.s.append(int(line[6]))
                    self.bx.append(float(line[2]))
                    self.by.append(float(line[3]))
                    self.bz.append(float(line[4]))
#                    self.bt.append(float(line[10]))
#                    self.lat.append(float(line[11]))
#                    self.lon.append(float(line[12]))
                    
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


    
    
class dscovr_class_web:
    def __init__(self):
        if os.sep=="/":
            osdir=os.sep+os.path.join("Users", "alyshareinard")
        else:
            osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard")
    
        rootdir=os.path.join(osdir, "Documents", "data", "DSCOVR")+os.sep
        
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
                
class dscovr_class_sql:
    def __init__(self, filename="dsc_mag1.txt"):
        if os.sep=="/":
            osdir=os.sep+os.path.join("Users", "alyshareinard")
        else:
            osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard")
    
        rootdir=os.path.join(osdir, "Documents", "data", "DSCOVR")+os.sep
        
        dscovr_file=os.path.join(rootdir, filename)
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
#                print(line)
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
 #               self.bt.append(float(line[2]))
                if line[2]=="NULL":
                    self.bx.append(None)
                else:
                    self.bx.append(float(line[2]))
                if line[3]=="NULL":
                    self.by.append(None)
                else:
                    self.by.append(float(line[3]))
                if line[4]=="NULL":
                    self.bz.append(None)
                else:
                    self.bz.append(float(line[4]))
#                self.lon.append(float(line[6]))
#                self.lat.append(float(line[7]))




#dscovr=dscovr_class_web()
#ace=ace_class_web()
#plot_bx_by_bz(ace, dscovr)

cc=[]
dates=[]
rmse=[]

parameter="Bz"
for month in range(2,9):
    print("ace_mag1_2016_0"+str(month)+".txt")
    dscovr=dscovr_class_sql(filename="dsc_mag1_2016_0"+str(month)+".txt")
    ace=ace_class_sql(filename="ace_mag1_2016_0"+str(month)+".txt")
#    print("dates", ace.date)




#plot_bt_lat_lon(ace, dscovr)
    first=datetime(2016, month, 1, 00, 00)
    start_date=[first+timedelta(days=x) for x in range(0,31)]

#start_date=datetime(2016, 6, 1, 00, 00)
#end_date=datetime(2016, 6, 2, 00, 00)

    for sd in start_date:
        ed=sd+timedelta(days=1)
        [this_cc, this_rmse]=scatter_plot(ace, dscovr, parameter, sd, ed) #options: lon, lon+120, lat, bt, bz
        if this_cc>0:
            cc.append(this_cc)
            rmse.append(this_rmse)
            dates.append(sd)
#        print(cc)

plt.plot(dates, rmse, "r.-")
plt.plot(dates, cc, "b.-")
plt.ylim([0,8])
plt.title("Correlation coefficient (blue) and RMSE (red) for ACE/DSCOVR "+parameter+", in 2016")





