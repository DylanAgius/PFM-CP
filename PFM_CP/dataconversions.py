# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 07:50:13 2020

@author: mi19356
"""

import numpy as np
import os
import pandas as pd
from collections import Counter


"""
Change the resolution of cells per grain
"""
def reso_change(vtkdata,dim):
    #first calculate the difference in volumes before and after the reso change
    #assuming the cell size is 1 cubed
    
    #count the occurance of grain index to form a volume
    ocgrain=Counter(vtkdata)
    
    #extract and reorder
    ocgrainids=np.array(list(ocgrain.items()))
    sortid=ocgrainids[:,0].argsort()
    ocgrainbefore=ocgrainids[sortid,1]
    
    #find the size of the array to reshape
    vtknshape=vtkdata.reshape(int(np.size(vtkdata)**0.5),int(np.size(vtkdata)**0.5))
    
    newvtk=vtknshape[::int(dim),::int(dim)].flatten()
    
    #count the occurance of grain index to form a volume
    ocgrainafter=Counter(newvtk)
    
    #extract and reorder
    ocgrainafterids=np.array(list(ocgrainafter.items()))
    sortidafter=ocgrainafterids[:,0].argsort()
    ocgrainafter=ocgrainafterids[sortidafter,1]
    

    
    #voldiff=ocgrainbefore/ocgrainafter
    
    
    
  
    return newvtk




"""
spherical diameter calculator
"""

def circlediam(vtkdata):

    #assumes the cell size is 1 cubed
    
    #count the occurance of grain index to form a volume
    ocgrain=Counter(vtkdata)
    
    #extract and reorder
    ocgrain=np.array(list(ocgrain.items()))
    sortid=ocgrain[:,0].argsort()
    ocgrain=ocgrain[sortid,1]

    #calculate the diameter
    diameter=2.*(((ocgrain)/np.pi)**(1/2))
    
    return diameter

"""
find the equivalent circle diameter
"""

def sphericaldiam(vtkdata):
    #assumes the cell size is 1 cubed
    
    #count the occurance of grain index to form a volume
    ocgrain=Counter(vtkdata)
    
    #extract and reorder
    ocgrain=np.array(list(ocgrain.items()))
    sortid=ocgrain[:,0].argsort()
    ocgrain=ocgrain[sortid,1]

    #calculate the diameter
    diameter=(((6*ocgrain)/np.pi)**(1/3))
    
    return diameter
   
""" 
alter and reconstruct vtk file
"""

def data_reconstruct(vtkdata,vtkdataPoints,orien):
    

    #remove floats which represent voxels at a grain boundary.
    
    #first find the floats
    floatloc=np.where(vtkdata != vtkdata.astype(int))[0]
    flotatdiff=np.diff(floatloc)
    
    #find the arrays which are not 1
    startendfloat=np.where(flotatdiff != 1)[0]
   
    nonones=floatloc[startendfloat+1]
    
    #adding the to the start of an array
    nonones=np.insert(nonones,0,floatloc[0])
    startendfloat=np.insert(startendfloat,0,-1)
    
   
    
    #find the length of cells containing the float
    floatlength=np.diff(startendfloat)
    
    #adding to the end of the array
    floatlength=np.insert(floatlength,np.size(floatlength),(np.size(flotatdiff)-startendfloat[-1]))
   
    for i in range(0,np.size(nonones)):
        halfval=int(floatlength[i]/2)
        vtkdata[nonones[i]:(nonones[i]+halfval)]=[vtkdata[nonones[i]-1]]*halfval
        vtkdata[(nonones[i]+halfval):(nonones[i]+floatlength[i])]=[vtkdata[nonones[i]+floatlength[i]]]*(floatlength[i]-halfval)
       
    #adjusting feature numbers to remove interface numbers
    #grain numbers
    grainids=orien[1:,0]-1
    
    grainidsdiff=np.diff(grainids)
    incwhere=np.where(grainidsdiff>2)
    
    grainids=np.insert(grainids,incwhere[0]+1,grainids[incwhere[0]]+2)
    
    #insert missing grain ids
    
    grainids=np.unique(vtkdata)
    
    
    
    for i in range(0,len(grainids)):
        location=np.where(vtkdata==grainids[i])
        vtkdata[location]=i+1
        
    
    sortedarray=np.sort(vtkdata)
    sortedarrayarg=np.argsort(vtkdata)
    
    sortinc=np.diff(sortedarray)
    incwhere=np.where(sortinc[:(len(sortinc)-1)]>1)
    
    valuesofint=sortedarrayarg[incwhere]
    vtkdataodd=vtkdata[valuesofint]
    
    #**test reso change
    #vtkdata=reso_change(vtkdata,2)
    

    
    #replace the grain id in the vtkdata with the index of the location in grain ids
    
        
    #now to reshape the array
    #vtkdata=vtkdata[::reso]
   # vtkdata=np.reshape(vtkdata,(int(np.size(vtkdata)/7),7))
    
    #readjusting te headers for vtk file for reading in
    headers=vtkdataPoints[1]
    #headers[1]=str('vtk output')
    #headers=np.insert(headers,5,str('CELL_DATA '))    
    
    voxlstring=list(vtkdataPoints[0])
    #convert to dataframe
    voxlstring=pd.DataFrame(voxlstring)
    voxlstring=np.asarray(voxlstring[0:])
    
    #number of headers at start
    headlen=len(headers)
        
  #  for i in range(0,np.size(voxlstring,axis=0)-1):
  #      headers.append(str(list(voxlstring[i].astype(int))).replace(',',' ')[1:-1])
    
    #headers=np.insert(headers,headlen+np.size(voxlstring,axis=0)-1,str('LOOKUP_TABLE default'))
    #headers=np.insert(headers,headlen+np.size(voxlstring,axis=0)-1,str('SCALARS FeatureIds int 1'))
    #headers=np.insert(headers,headlen+np.size(voxlstring,axis=0)-1,str('POINT_DATA 1002001'))
    
    headers=np.insert(headers,headlen,str('LOOKUP_TABLE default'))
    headers=np.insert(headers,headlen,str('SCALARS FeatureIds int 1'))
    headers=np.insert(headers,headlen,str('POINT_DATA 1002001'))
    headers=np.insert(headers,headlen,str('ORIGIN 0 0 0'))
    headers=np.insert(headers,headlen,str('SPACING 1 1 1'))
    
    headers=vtkdata.astype(int)
 
    printtofile(headers,'new')
   
    
    return grainids



def printtofiletext(array,name):
    loc=os.path.join(os.path.dirname(__file__),'data')
    with open(os.path.join(loc,name + '.txt'), 'w') as f:
        for item in array:
            f.write("%s\n" % item)
                
        
        

def printtofile(array,name):
    loc=os.path.join(os.path.dirname(__file__),'data')
    with open(os.path.join(loc,name + '.vtk'), 'w') as f:
        for item in array:
            f.write("%s\n" % item)
    

    
    
    



