# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 08:04:57 2020

@author: mi19356
"""

from argparse import ArgumentParser
import numpy as np

parser = ArgumentParser()


parser.add_argument('-a', dest='cname',
                    help="Name of vtk file", type=str)
parser.add_argument('-b',dest='ename',help="Name of angles",type=str)

args = parser.parse_args()

