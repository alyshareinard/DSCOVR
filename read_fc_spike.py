# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 16:25:58 2016

@author: alysha.reinard
"""
import csv
import os
import matplotlib.pyplot as plt
import datetime
import numpy as np
import numpy.ma as ma

def read_ace(filename, dscovr_date):
    if os.sep=="/":
        osdir=os.sep+os.path.join("Users", "alyshareinard")
    else:
        osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard")
    rootdir=os.path.join(osdir, "Documents")+os.sep
    print("fulldir", rootdir+filename)
    
    timestamp=[]
    density=[]
    speed=[]  
    temperature=[]
    vx=[]
    vy=[]
    vz=[]

    with open(rootdir+filename, 'r', encoding="utf-8") as csvfile:
        data=csv.reader(csvfile, delimiter=',', quotechar="|")
        for i in range(23): header=data.__next__()
        print("ACE header", header)
        for line in data:
            print("line", line)
            if line[0]=="":
                continue
            year=int(line[0])
            doy=float(line[1])+float(line[2])
            date=datetime.datetime(year, 1, 1)+datetime.timedelta(doy-1)
            if date>min(dscovr_date) and date<max(dscovr_date):
                timestamp.append(date)
                print(timestamp[-1])
                density.append(float(line[3]))
                speed.append(float(line[5]))
                temperature.append(float(line[4]))
                vx.append(float(line[6]))
                vy.append(float(line[7]))
                vz.append(float(line[8]))
    print("DSCOVR DATES", min(dscovr_date), max(dscovr_date))
    ace={"timestamp":timestamp, "density":density, "speed":speed, "temperature":temperature, "vx":vx, "vy":vy, "vz":vz}
    return ace

def read_ace_browse(filename, dscovr_date):
    if os.sep=="/":
        osdir=os.sep+os.path.join("Users", "alyshareinard")
    else:
        osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard")
    rootdir=os.path.join(osdir, "Documents")+os.sep
    print("fulldir", rootdir+filename)
    
    timestamp=[]
    density=[]
    speed=[]  
    temperature=[]

    with open(rootdir+filename, 'r', encoding="utf-8") as csvfile:
        data=csv.reader(csvfile, delimiter=',', quotechar="|")
        for i in range(23): header=data.__next__()
#        print("header", header)
        for line in data:
#            print("line", line)
            year=int(line[0])
            doy=float(line[1])
            date=datetime.datetime(year, 1, 1)+datetime.timedelta(doy-1)
            if date>min(dscovr_date) and date<max(dscovr_date):
                timestamp.append(date)
                print(timestamp[-1])
                density.append(float(line[2]))
                speed.append(float(line[3]))
                temperature.append(float(line[4]))
    print("DSCOVR DATES", min(dscovr_date), max(dscovr_date))
    ace={"timestamp":timestamp, "density":density, "speed":speed, "temperature":temperature}
    return ace
    
def read_fc(filename):
    
    if os.sep=="/":
        osdir=os.sep+os.path.join("Users", "alyshareinard")
    else:
        osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard")
    rootdir=os.path.join(osdir, "Documents")+os.sep
    print("fulldir", rootdir+filename)

    timestamp=[]
    modlow=[]
    currents=[]
    start_peak_end=[]
    width_count=[]
    speed=[]
    density=[]
    temperature=[]
    peak_pa=[]

    with open(rootdir+filename, 'r', encoding="utf-8") as csvfile:
        data=csv.reader(csvfile, delimiter=',', quotechar="|")
        header=data.__next__()
        print("header", header)
        for line in data:
            date=line[0]
            date=date.replace(':', '-').replace(' ', '-').replace('T', '-').replace('Z', '').split('-')
            dateints=[int(round(float(x))) for x in date]
#            print("dateints", dateints)
            if dateints[5]==60:
                dateints[5]=0
                dateints[4]=dateints[4]+1
            if dateints[4]==60:
                dateints[4]=0
                dateints[3]=dateints[3]+1
            if dateints[3]==24:
                dateints[3]=0   
                dateints[2]=dateints[2]+1
            if dateints[2]==13:
                dateints[2]=1
                dateints[1]=dateints[1]+1
            timestamp.append(datetime.datetime(dateints[0], dateints[1], dateints[2], dateints[3], dateints[4], dateints[5]))
            modlow.append(int(line[1]))
            curvals=line[3:26]
#            print("curvals", curvals)
#            curvals=["0" for x in curvals if x==""]
            curvals=[0.0 if x=="" else float(x) for x in curvals]
            currents.append(curvals)
            start_peak_end.append([int(line[27]), int(line[29]), int(line[33])])
 #           print("SPE", start_peak_end)
            width_count.append([int(line[35]), int(line[37])])
            speed.append(int(line[40]))
#            print("density?", line[41])
            density.append(float(line[41]))
            temperature.append(float(line[42]))

            peak_pa.append(float(line[47]))

    dscovr={"timestamp":timestamp, "modlow":modlow, "currents":currents, 
            "spe":start_peak_end, "wc":width_count, "speed":speed, 
            "density":density, "temperature":temperature, "peak_pa":peak_pa}
    return dscovr
            
#    print(overall_quality)
#    plt.plot(timestamp, speed)
            
def find_dscovr_anomalies(dscovr, ace):
    dsc_time=dscovr["timestamp"]
    dsc_speed=dscovr["speed"]
    ace_time=ace["timestamp"]
    ace_speed=ace["speed"]
    dsc_dens=dscovr["density"]

    dsc_vel_TF=[]
    ace_speed_long=[]

    #we find the closest ace time for each dscovr time
    for dsc_ind, time in enumerate(dsc_time):
        timediff=[abs(time-x) for x in ace_time] #might need to make numpy
        ace_ind=timediff.index(min(timediff))
#        print("index", ace_ind)
        #here we look and see how far the ace and dscovr speeds are apart
        speed_diff=dsc_speed[dsc_ind]-ace_speed[ace_ind]
        ace_speed_long.append(ace_speed[ace_ind])
        if speed_diff>40:
            dsc_vel_TF.append(False)
        else:
            dsc_vel_TF.append(True)


    dens_np=np.array(dscovr["density"])
    low_dens=dens_np>1.1 #masks are the reverse
    high_dens=dens_np<=1.1
    
    ace_high=ma.array(ace_speed_long)
    ace_high.mask=high_dens
    
    ace_low=ma.array(ace_speed_long)
    ace_low.mask=low_dens

    dsc_high=ma.array(dsc_speed)
    dsc_high.mask=high_dens

    dsc_low=ma.array(dsc_speed)
    dsc_low.mask=low_dens
    
    plt.figure(0)
    
    plt.scatter(ace_low, dsc_low, alpha=0.5, color="red")
    plt.scatter(ace_high, dsc_high, alpha=0.5, color="green")
    return dsc_vel_TF




#    plt.figure(3)
#    plt.plot(dsc_time, speed_diff)
#    print("dscovr", dsc_time[0])
#    print("ace", ace_time[0])
#    print(timediff)

    
def make_plots(dscovr, ace):
    dscovr_plots=False
    
    dsc_mask=dscovr["TF"]
    not_dsc_mask=[not x for x in dsc_mask]

    plt.figure(10)
    plt.plot(ace["timestamp"], ace["speed"], "blue")
    plt.plot(dscovr["timestamp"], dscovr["speed"], "green")    
    
    density_high=ma.array(dscovr["density"])
    density_high.mask=not_dsc_mask

    density_low=ma.array(dscovr["density"])
    density_low.mask=dsc_mask

    pa_high=ma.array(dscovr["peak_pa"])
    pa_high.mask=not_dsc_mask


    pa_low=ma.array(dscovr["peak_pa"])
    pa_low.mask=dsc_mask

    speed_high=ma.array(dscovr["speed"])
    speed_high.mask=not_dsc_mask

    speed_low=ma.array(dscovr["speed"])
    speed_low.mask=dsc_mask
    
    timestamp_high=ma.array(dscovr["timestamp"])
    timestamp_high.mask=not_dsc_mask

    timestamp_low=ma.array(dscovr["timestamp"])
    timestamp_low.mask=dsc_mask

    width=[x[0] for x in dscovr["wc"]]
    
    width_high=ma.array(width)
    width_high.mask=not_dsc_mask

    width_low=ma.array(width)
    width_low.mask=dsc_mask    

    plt.figure(4)
    plt.scatter(speed_high, pa_high, alpha=0.5, s=2, color="green")
    plt.scatter(speed_low, pa_low, alpha=0.5, s=2, color="red")
    plt.show()

    plt.figure(5)
    plt.scatter(density_low, pa_low, alpha=0.5, s=4, color="red")
    plt.scatter(density_high, pa_high, alpha=0.5, s=8, color="green")
    plt.show()


    plt.figure(6)
    plt.plot(timestamp_high, speed_high, color="green")
    plt.plot(timestamp_low, speed_low, color="red")        
    
    plt.figure(7)
    bin_vals=range(10)
    plt.hist(width_low.compressed(), color="red", alpha=0.5, label="good", bins=bin_vals)
    plt.hist(width_high.compressed(), color="green", alpha=0.5, label="high", bins=bin_vals)
    plt.show()

    bin_vals=[x/10. for x in range(10)]   
    plt.figure(8)
    plt.hist(density_low.compressed(), color="red", alpha=0.5)#, label="good", bins=bin_vals)
    plt.hist(density_high.compressed(), color="green", alpha=0.5)#, label="high", bins=bin_vals)
    plt.show()    

    plt.figure(9)
    bin_vals=range(10)
    plt.hist(pa_low.compressed(), color="red", alpha=0.5)#, label="good", bins=bin_vals)
    plt.hist(pa_high.compressed(), color="green", alpha=0.5)#, label="high", bins=bin_vals)
    plt.show() 
    
    if dscovr_plots==True:
        plt.figure(0)
        plt.scatter(dscovr["speed"], dscovr["density"], alpha=0.5, s=2)
        plt.xlabel="speed"
        plt.ylabel="density"
        plt.show()
        plt.figure(1)
        plt.scatter(dscovr["speed"], dscovr["peak_pa"], alpha=0.5, s=2)
        plt.xlabel="speed"
        plt.ylabel="peak_pa"
        plt.show()
        speed_np=np.array(dscovr["speed"])
    
        high_ind=speed_np>500
        med_ind=np.logical_and(speed_np>430, speed_np<=500)
        low_ind=speed_np<=430
        
        high_mask=[not x for x in high_ind]
        med_mask=[not x for x in med_ind]
        low_mask=[not x for x in low_ind]
    #https://docs.scipy.org/doc/numpy/reference/maskedarray.generic.html#maskedarray-generic-constructing
        
        density_high=ma.array(dscovr["density"])
        density_high.mask=high_mask
        
        density_med=ma.array(dscovr["density"])
        density_med.mask=med_mask
    
        density_low=ma.array(dscovr["density"])
        density_low.mask=low_mask
        
        
        pa_high=ma.array(dscovr["peak_pa"])
        pa_high.mask=high_mask
    
        pa_med=ma.array(dscovr["peak_pa"])
        pa_med.mask=med_mask
    
        pa_low=ma.array(dscovr["peak_pa"])
        pa_low.mask=low_mask
    
        speed_high=ma.array(dscovr["speed"])
        speed_high.mask=high_mask
    
        speed_med=ma.array(dscovr["speed"])
        speed_med.mask=med_mask
    
        speed_low=ma.array(dscovr["speed"])
        speed_low.mask=low_mask
    
    
    #    print(density[high_ind] )
        plt.figure(2)
        plt.scatter(speed_med, pa_med, alpha=0.5, s=2, color="yellow")
        plt.scatter(speed_low, pa_low, alpha=0.5, s=2, color="green")
        plt.scatter(speed_high, pa_high, alpha=0.5, s=2, color="red")
        plt.show()
    
        plt.figure(3)
        plt.scatter(density_med, pa_med, alpha=0.5, s=2, color="yellow")
        plt.scatter(density_low, pa_low, alpha=0.5, s=2, color="green")
        plt.scatter(density_high, pa_high, alpha=0.5, s=2, color="red")
        plt.show()
        
        dens_np=np.array(dscovr["density"])
        low_dens=dens_np>1.1 #masks are the reverse
        high_dens=dens_np<=1.1
        
        density_high=ma.array(dscovr["density"])
        density_high.mask=high_dens
    
        density_low=ma.array(dscovr["density"])
        density_low.mask=low_dens    
    
        pa_high=ma.array(dscovr["peak_pa"])
        pa_high.mask=high_dens
    
    
        pa_low=ma.array(dscovr["peak_pa"])
        pa_low.mask=low_dens
    
        speed_high=ma.array(dscovr["speed"])
        speed_high.mask=high_dens
    
        speed_low=ma.array(dscovr["speed"])
        speed_low.mask=low_dens
        
        timestamp_high=ma.array(dscovr["timestamp"])
        timestamp_high.mask=high_dens
    
        timestamp_low=ma.array(dscovr["timestamp"])
        timestamp_low.mask=low_dens
    
        plt.figure(4)
        plt.scatter(speed_low, pa_low, alpha=0.5, s=2, color="red")
        plt.scatter(speed_high, pa_high, alpha=0.5, s=2, color="green")
        plt.show()
    
        plt.figure(5)
        plt.scatter(density_low, pa_low, alpha=0.5, s=2, color="red")
        plt.scatter(density_high, pa_high, alpha=0.5, s=2, color="green")
        plt.show()
    
    
        plt.figure(6)
        plt.plot(timestamp_high, speed_high, color="green")
        plt.plot(timestamp_low, speed_low, color="red")

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
        
dscovr=read_fc("fc_spike_analysis.csv")
ace=read_ace_browse("ACE_Browse_Data.csv", dscovr["timestamp"])
ace=read_ace("ace_2016336.csv", dscovr["timestamp"])

dscovr["TF"]=find_dscovr_anomalies(dscovr, ace)
make_plots(dscovr, ace)
