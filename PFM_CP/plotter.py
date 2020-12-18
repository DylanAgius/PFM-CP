# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 18:08:17 2020

@author: mi19356
"""
import numpy as np
import os
import pandas as pd

from pymicro.crystal.texture import PoleFigure
from pymicro.crystal.microstructure import Microstructure, Grain, Orientation
from matplotlib import pyplot as plt

'''
A pole figure plotted using contours.
'''
def printtofiletext(array,name):
    loc=os.path.join(os.path.dirname(__file__),'data')
    with open(os.path.join(loc,name + '.txt'), 'w') as f:
        for item in array:
            f.write("%s\n" % ' '.join(map(str, item)))

def polefig(orien):
    
    eulers = orien[:,1:]
    
    printtofiletext(eulers,'test')
    