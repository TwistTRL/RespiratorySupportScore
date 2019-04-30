#!/usr/bin/env python

def calculateETCategory(airwayDeviceSize):
  if "mapping" not in calculateETCategory.__dict__:
    calculateETCategory.mapping = {
      "1":    1,
      "1.5":	1,
      "2":	  1,
      "2.5":	1,
      "3":	  1,
      "3.5":	1,
      "4":	  2,
      "4.5":	2,
      "5":	  3,
      "5.5":	3,
      "6":	  3,
      "6.5":	3,
      "7":	  3,
      "7.5":	3,
      "8":	  3
    }
  return calculateETCategory.mapping.get(airwayDeviceSize,0)
