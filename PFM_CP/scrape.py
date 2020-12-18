# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 05:36:16 2020

@author: mi19356
"""
import numpy as np
import os
import pandas as pd


def vtk_scrape(cname,ename,delim):
     loc=os.path.join(os.path.dirname(__file__),'data')
     
     #read in vtk file information
     vtkdata=np.array(vtkread(os.path.join(loc,cname + '.vtk'))).astype(np.float64)
     vtkdataPoints=np.array(vtkread2(os.path.join(loc,cname + '.vtk'),' '))

     #read in orientation data
     angles=np.array(file_read(os.path.join(loc,ename + '.'+delim),' : '))
     anglesadjs=angles[:,1:].astype(np.float64)
     
     
     return anglesadjs,vtkdata,vtkdataPoints

"""
VTK file reader for grain ids
"""
def vtkread(fname):
        start=0
        prevline=""
        content_array=[]
        storeheaders=[]
        checker=0
        file_end=0
        with open(fname) as textFile:
           
            for line in textFile :
                if "SCALARS PhaseFields double 1" in line:
                    checker=1
                if "SCALARS PhaseFraction_0 double 1" in line:
                    break
                if ("LOOKUP_TABLE default" in prevline) & checker==1:
             
                    checker=0
                    start=1
                
                if start==1:
                    #content_array=np.append(content_array,[line.split(delim)])
                    content_array.append(line)
                #else:
                    #storeheaders.append(line)
                    
                prevline=line
        
               
        return content_array
    
"""
VTK file reader for pointdata
"""

def vtkread2(fname,delim):
        start=0
        prevline=""
        content_array=[]
        storeheaders=[]
        with open(fname) as textFile:
            for line in textFile :
                if "POINT_DATA" in line:
                    break
                if "POINTS" in prevline:
                    start=1
                if start==1:
                    content_array.append(line.split(delim))
                else:
                    storeheaders.append(line)
                    
                prevline=line
            
               
        return content_array,storeheaders
    
def file_read(fname,delim):
        with open(fname) as textFile:
            content_array = [line.split(delim) for line in textFile]
               
        return (content_array)
    
