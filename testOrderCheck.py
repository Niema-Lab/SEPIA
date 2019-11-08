#!/usr/bin/env python3
from orderCheck import *

infectionsDict = countInfections("01.transmissions.txt", 0, 5)

userSortedInfectors = ['CNG0-COM0-92','CNG0-COM17-1425','CNG0-COM12-92','CNG0-COM11-190']

userSortedCounts  = matchInfectorCounts(infectionsDict, userSortedInfectors)

infectionsValues = infectionsDict.values()

#calculateTauB(infectionsValues, userSortedCounts)
