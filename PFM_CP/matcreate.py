# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:19:55 2020

@author: mi19356
"""

import numpy as np
import os
import pandas as pd
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree
import random
import math

from scrape import vtk_scrap
from dataconversions import data_reconstruct, reso_change, data_reconstruct_dream,sphericaldiam,printtofiletext

#scrape data
#orien,vtkdata,vtkdataPoints,const=vtk_scrap('PF_00189000','graindata') 
dream=0
if dream==1:
    orien,vtkdata,vtkdataPoints,const=vtk_scrap('PF_00130000','graindata',dream) 
    grainids=data_reconstruct(vtkdata, vtkdataPoints,1,orien)
else:
    orien,vtkdata,const=vtk_scrap('vtkupdate','graindata',dream)
    grainids,diameter=data_reconstruct_dream(vtkdata,orien)
    
#construct a vtk file
#vtkdatareso=reso_change(vtkdata)


"""
Create orientatio matrix
"""

def rotation_info(orien,grainids):
     
   
     
     
     #Defining local variables
    
     vec1=[0,0,1]
     vec2=[0,1,0]
     
     #modify the orientations
     orien=orien[1:,1:]
     
     #check to see if there are missing orientations
     if len(orien)<len(grainids):
         totaldif=len(grainids)-len(orien)
         for i in range(0,int(totaldif)):
             orien=np.append(orien,[random.uniform(0,2*math.pi),random.uniform(0,2*math.pi),random.uniform(0,2*math.pi)])
     orien=orien.reshape(int(len(orien)/3),3)
    
     #contruct rotation matrix
     
     zrot=np.array([[np.cos((orien[:,0])),np.sin((orien[:,0])),np.zeros(len(orien))],[-np.sin((orien[:,0])),np.cos((orien[:,0])),np.zeros(len(orien))],[np.zeros(len(orien)),np.zeros(len(orien)),np.ones(len(orien))]])
     xrot=np.array([[np.ones(len(orien)),np.zeros(len(orien)),np.zeros(len(orien))],[np.zeros(len(orien)),np.cos((orien[:,1])),np.sin((orien[:,1]))],[np.zeros(len(orien)),-np.sin((orien[:,1])),np.cos((orien[:,1]))]])
     zrot2=np.array([[np.cos((orien[:,2])),np.sin((orien[:,2])),np.zeros(len(orien))],[-np.sin((orien[:,2])),np.cos((orien[:,2])),np.zeros(len(orien))],[np.zeros(len(orien)),np.zeros(len(orien)),np.ones(len(orien))]])
     
     total_rot=[[]*len(orien)]*len(orien)
     samp1=[[]*len(orien)]*len(orien)
     samp2=[[]*len(orien)]*len(orien) 
     
     for i in range(0,len(orien)):
     
         total_rot[i]=np.transpose(np.dot(np.dot(zrot2[:,:,i],xrot[:,:,i]),zrot[:,:,i]))
         samp1[i]=np.dot(total_rot[i],vec1)
         samp2[i]=np.dot(total_rot[i],vec2)
         
  
     
     return vec1, vec2, samp1, samp2, total_rot, orien
 
 
"""
create material file for AMITEX
"""    

def mat_create(orien,const, diameter,statev):
    
    #rotating vectors using grain orientations
    vec1,vec2,samp1,samp2,total_rot, orien=rotation_info(orien,grainids)
    
    #use the diameter to create a variable parameter for \tau
    #diameter currnetly in microns, convert to mm
    
    #need to add 17.9 and 10 to excel const file.
    diameter=(2*diameter)/1000
    
    #writing diameters to file
    printtofiletext(diameter,'diameters')
    
    #writing orientations to file
    orienprint=list(orien)
    printtofiletext(orienprint,'orientations')
    
    taud=220 + (17.9/((diameter)**0.5))
    
    #check to make sure the there are no 
    #checkgreater=np.where(taud>350)[0]
    #replace these values
    #taud[checkgreater]=340.0


    Materials = Element('Materials')
    comment = Comment('REFERENCE MATERIAL')
    Materials.append(comment)

    child = SubElement(Materials, 'Reference_Material',Lambda0= '2.0431e+5', Mu0='0.8756e+5' )

    comment = Comment('MATERIAL 1')
    Materials.append(comment)

    "orientation files required if material zone technique is used in AMITEX"
    fsamp1 = open('fsam1.txt', 'w')
    fsamp2 = open('fsam2.txt', 'w')
    fsamp3 = open('fsam3.txt', 'w')
    fsamp21 = open('fsam21.txt', 'w')
    fsamp22 = open('fsam22.txt', 'w')
    fsamp23 = open('fsam23.txt', 'w')
    orien1 = open('orien1.txt', 'w')
    orien2 = open('orien2.txt', 'w')
    orien3 = open('orien3.txt', 'w')
    tau01 = open('tau1.txt', 'w')
    tau02 = open('tau2.txt', 'w')

    for numMat in range(1,len(orien)+1):
 
        for i in range(0,(len(const))):
            if i==59:
                const[i,0]=samp1[numMat-1][0]
                fsamp1.write(str("{:.16f}".format(const[i,0]))+'\n')
            elif i==60:
                const[i,0]=samp1[numMat-1][1]
                fsamp2.write(str("{:.16f}".format(const[i,0]))+'\n')
            elif i==61:
                const[i,0]=samp1[numMat-1][2]
                fsamp3.write(str("{:.16f}".format(const[i,0]))+'\n')
            elif i==67:
                const[i,0]=samp2[numMat-1][0]
                fsamp21.write(str("{:.16f}".format(const[i,0]))+'\n')
            elif i==68:
                const[i,0]=samp2[numMat-1][1]
                fsamp22.write(str("{:.16f}".format(const[i,0]))+'\n')
            elif i==69:
                const[i,0]=samp2[numMat-1][2]
                fsamp23.write(str("{:.16f}".format(const[i,0]))+'\n')
                #adjust const array to include grain dependent info    
                #grain orientations
            #update the value for tau0
            elif i==98:
                const[i,0]=taud[numMat-1]
                tau01.write(str("{:.16f}".format(const[i,0]))+'\n')
            elif i==114:
                const[i,0]=taud[numMat-1]
                tau02.write(str("{:.16f}".format(const[i,0]))+'\n')
            elif i==168:
                const[i,0]=(orien[numMat-1,0])
                orien1.write(str(const[i,0])+'\n')
            elif i==169:
                const[i,0]=(orien[numMat-1,1])
                orien2.write(str(const[i,0])+'\n')
            elif i==170:
                const[i,0]=(orien[numMat-1,2])
                orien3.write(str(const[i,0])+'\n')
     
     
    fsamp1.close()
    fsamp2.close()
    fsamp3.close()
    fsamp21.close()
    fsamp22.close()
    fsamp23.close()
    orien1.close()
    orien2.close()
    orien3.close()

    child_grain=SubElement(Materials, 'Material', numM="1",Lib='/mnt/storage/home/mi19356/amitex_fftp-v8.17.1/Grainsize/UMAT/libUmatAmitex.so', Law='UMATBCCGDGS')

    "This stores all the parameters required for the material"
    "Coeff is the element of the grain material, and the atrributes are the parameter values"

    "iterate across the different material constants to create subelelements for each constant2"
    
    for i in range(0,(len(const))):
        if i==59:
            const[i,0]=samp1[numMat-1][0]
            child_grain_tail = SubElement(child_grain, 'Coeff',Index=str(i+1), Type='Constant_Zone', File="MAT/Coeff/fsam1.txt")
        elif i==60:
            const[i,0]=samp1[numMat-1][1]
            child_grain_tail = SubElement(child_grain, 'Coeff',Index=str(i+1), Type='Constant_Zone', File="MAT/Coeff/fsam2.txt")
    
        elif i==61:
            const[i,0]=samp1[numMat-1][2]
            child_grain_tail = SubElement(child_grain, 'Coeff',Index=str(i+1), Type='Constant_Zone', File="MAT/Coeff/fsam3.txt")
    
        elif i==67:
            const[i,0]=samp2[numMat-1][0]
            child_grain_tail = SubElement(child_grain, 'Coeff',Index=str(i+1), Type='Constant_Zone', File="MAT/Coeff/fsam21.txt")
        
        elif i==68:
            const[i,0]=samp2[numMat-1][1]
            child_grain_tail = SubElement(child_grain, 'Coeff',Index=str(i+1), Type='Constant_Zone', File="MAT/Coeff/fsam22.txt")
 
        elif i==69:
            const[i,0]=samp2[numMat-1][2]
            child_grain_tail = SubElement(child_grain, 'Coeff',Index=str(i+1), Type='Constant_Zone', File="MAT/Coeff/fsam23.txt")

        elif i==98:
            const[i,0]=taud[numMat-1]
            child_grain_tail = SubElement(child_grain, 'Coeff',Index=str(i+1), Type='Constant_Zone', File="MAT/Coeff/tau1.txt")
        elif i==114:
            const[i,0]=taud[numMat-1]
            child_grain_tail = SubElement(child_grain, 'Coeff',Index=str(i+1), Type='Constant_Zone', File="MAT/Coeff/tau2.txt")

        
        elif i==168:
            const[i,0]=(orien[numMat-1,0])
            child_grain_tail = SubElement(child_grain, 'Coeff',Index=str(i+1), Type='Constant_Zone', File="MAT/Coeff/orien1.txt")

        elif i==169:
            const[i,0]=(orien[numMat-1,1])
            child_grain_tail = SubElement(child_grain, 'Coeff',Index=str(i+1), Type='Constant_Zone', File="MAT/Coeff/orien2.txt")
  
        elif i==170:
            const[i,0]=(orien[numMat-1,2])
            child_grain_tail = SubElement(child_grain, 'Coeff',Index=str(i+1), Type='Constant_Zone', File="MAT/Coeff/orien3.txt")

        
       
        else:
            child_grain_tail = SubElement(child_grain, 'Coeff',Index=str(i+1), Type='Constant',Value=str(const[i,0]))
  

#iterate across the required number of state vairables needed 
    for i in range(0,statev):
        child_grain_tail = SubElement(child_grain, 'IntVar',Index=str(i+1), Type='Constant',Value='0.')

    tree = ElementTree(Materials)
    tree.write("fatemptzone2.xml")


mat_create(orien,const,diameter,900)
