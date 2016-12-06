# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 16:25:58 2016

@author: alysha.reinard
"""
import csv
import os
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import numpy.ma as ma

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
            timestamp.append(datetime(dateints[0], dateints[1], dateints[2], dateints[3], dateints[4], dateints[5]))
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

            
#    print(overall_quality)
#    plt.plot(timestamp, speed)
    plt.scatter(speed, density, alpha=0.5, s=2)
    plt.xlabel="speed"
    plt.ylabel="density"
    plt.show()
    plt.scatter(speed, peak_pa, alpha=0.5, s=2)
    plt.xlabel="speed"
    plt.ylabel="peak_pa"
    plt.show()
    speed_np=np.array(speed)

    high_ind=[speed_np>500]
    med_ind=[np.logical_and(speed_np>430, speed_np<=500)]
    low_ind=[speed_np<=430]
#https://docs.scipy.org/doc/numpy/reference/maskedarray.generic.html#maskedarray-generic-constructing
    
    density_high=ma.array(density)
    density_high.mask=~high_ind
    
    density_med=ma.array(density)
    density_med.mask=~med_ind

    density_low=ma.array(density)
    density_low.mask=~low_ind
    
    
    pa_high=ma.array(peak_pa)
    pa_high.mask=~high_ind

    pa_med=ma.array(peak_pa)
    pa_med.mask=~med_ind

    pa_low=ma.array(peak_pa)
    pa_low.mask=~low_ind

    speed_high=ma.array(speed)
    speed_high.mask=~high_ind

    speed_med=ma.array(speed)
    speed_med.mask=~med_ind

    speed_low=ma.array(speed)
    speed_low.mask=~low_ind
    
#    print(high_ind)
#    print(density[high_ind] )

    plt.scatter(speed_med, pa_med, alpha=0.5, s=2, color="yellow")
    plt.scatter(speed_low, pa_low, alpha=0.5, s=2, color="green")
    plt.scatter(speed_high, pa_high, alpha=0.5, s=2, color="red")
    plt.show()

    plt.scatter(density_med, pa_med, alpha=0.5, s=2, color="yellow")
    plt.scatter(density_low, pa_low, alpha=0.5, s=2, color="green")
    plt.scatter(density_high, pa_high, alpha=0.5, s=2, color="red")
    plt.show()
    
    
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
read_fc("fc_spike_analysis.csv")