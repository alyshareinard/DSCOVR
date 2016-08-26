# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 16:25:58 2016

@author: alysha.reinard
"""

def read_fc_out():
    
    if os.sep=="/":
        osdir=os.sep+os.path.join("Users", "alyshareinard")
    else:
        osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard.SWPC")

    rootdir=os.path.join(osdir, "Dropbox", "Work", "data", "DSCOVR")+os.sep
    print("fulldir", rootdir)
    data=readsav(rootdir+"fc_out.csv")

    timestamp=[]
    start=[]
    peak=[]
    end=[]
    left=[]
    right=[]
    width=[]

    for line in data:
        vals=line.split()
        print(vals)