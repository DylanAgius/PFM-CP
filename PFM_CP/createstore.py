# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 19:08:12 2020

@author: mi19356
"""
import numpy as np
import os
import pandas as pd

from scrape import vtk_scrape
from dataconversions import data_reconstruct,reso_change
from plotter import polefig



"""
Scraping all necessary data where:
    >'PF_00130000' is the name of the VTK file
    >'graindata' is the name of the grain orientation data
    >'inp' is the file extension for the grain orientation data
"""
anglesadjs,vtkdata,vtkdataPoints=vtk_scrape('PF_00064000','graindata','inp')

"""
function used to change resolution of the number of cells per grain where:
    >dim is the dimension of the resolution
"""
dim=2
vtkdata=reso_change(vtkdata,dim)
#test=1

#polefig(anglesadjs)

grainids=data_reconstruct(vtkdata,vtkdataPoints,anglesadjs)