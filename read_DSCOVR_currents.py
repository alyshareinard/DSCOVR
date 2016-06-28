# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 10:06:43 2016

@author: alysha.reinard
"""

import sys
sys.path.append('../common/')
from scipy.io.idl import readsav
import os
from datetime import datetime, timezone
from sunpy_time import parse_time

def read_DSCOVR_currents():

    if os.sep=="/":
        osdir=os.sep+os.path.join("Users", "alyshareinard")
    else:
        osdir=os.path.join("C:"+os.sep+"Users", "alysha.reinard.SWPC")

    rootdir=os.path.join(osdir, "Dropbox", "Work", "IDL_code", "analysis", "DSCOVR")+os.sep
    print("fulldir", rootdir)
    data=readsav(rootdir+"faraday_cup.sav")
    print(data)
