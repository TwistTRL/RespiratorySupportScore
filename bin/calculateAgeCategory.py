#!/usr/bin/env python

def calculateAgeCategory(age_sec):
  if age_day < 30*24*60*60:
    return 1
  if age_day < 365*24*60*60:
    return 2
  if age_day < 4380*24*60*60:
    return 3
  if age_day < 6570*24*60*60:
    return 4
  if age_day < 55000*24*60*60:
    return 5
