#!/usr/bin/env python

import pandas as pd
import time
import numpy as np

RSV = [ "Percent FiO2","__NC_Flow","HFNC Flow","__MASK_Flow",
        "Bubble Set CPAP","BiPAP IPAP Setting","BiPAP EPAP Setting",
        "BiPAP Rate","PIP Calculation","Apollo PEEP","Pressure Support",
        "Ventilator Rate","Tidal Volume","VT-Spontaneous (mL)",
        "VT-Mandatory (mL)","HFJV Monitored PEEP","HFJV_PIP",
        "HFJV Rate","HFOV Amplitude","HFOV Frequency"
        ];

def fillMeasurements(df):
  print(df.head())
  if df.shape[0]<=1:
    return df
  recordList = list(df.to_dict(orient="records"))
  prevRow = {"RST":None}
  for row in recordList:
    if row["RST"]==prevRow["RST"]:
      for rsv in RSV:
        if rsv in row and row[rsv]=="":
          row[rsv] = prevRow[rsv]
    prevRow = row
  prevRow = {"RST":None}
  for row in recordList[::-1]:
    if row["RST"]==prevRow["RST"]:
      for rsv in RSV:
        if rsv in row and row[rsv]=="":
          row[rsv] = prevRow[rsv]
    prevRow = row
  newDF = pd.DataFrame(recordList)
  print(newDF.head())
  return newDF
  
def calculateAgeCategory(age_sec):
  if age_sec < 30*24*60*60:
    return 1
  if age_sec < 365*24*60*60:
    return 2
  if age_sec < 4380*24*60*60:
    return 3
  if age_sec < 6570*24*60*60:
    return 4
  if age_sec < 55000*24*60*60:
    return 5

def calculateETCategory(airwayDeviceSize):
  if "mapping" not in calculateETCategory.__dict__:
    calculateETCategory.mapping = {
      "1":    1,
      "1.5":  1,
      "2":    1,
      "2.5":  1,
      "3":    1,
      "3.5":  1,
      "4":    2,
      "4.5":  2,
      "5":    3,
      "5.5":  3,
      "6":    3,
      "6.5":  3,
      "7":    3,
      "7.5":  3,
      "8":    3
    }
  return calculateETCategory.mapping.get(airwayDeviceSize,0)
  
def calculateRespiratorySupportScore(record):
  if "RSV_order" not in calculateRespiratorySupportScore.__dict__:
    calculateRespiratorySupportScore.RSV_order = ["Percent FiO2",
                                      "__NC_Flow",
                                      "HFNC Flow",
                                      "__MASK_Flow",
                                      "Bubble Set CPAP",
                                      "BiPAP IPAP Setting",
                                      "BiPAP EPAP Setting",
                                      "BiPAP Rate",
                                      "PIP Calculation",
                                      "Apollo PEEP",
                                      "Pressure Support",
                                      "Ventilator Rate",
                                      "Tidal Volume",
                                      "VT-Spontaneous (mL)",
                                      "VT-Mandatory (mL)",
                                      "HFJV Monitored PEEP",
                                      "HFJV_PIP",
                                      "HFJV Rate",
                                      "HFOV Amplitude",
                                      "HFOV Frequency"]
  if "RSV_bounds" not in calculateRespiratorySupportScore.__dict__:
    df = pd.read_csv("./config/RSV_Bounds.tsv",sep='\t')
    bounds = {}
    for i,row in df.iterrows():
      print()
      age_cat = row["age_cat"]
      ET_cat = row["ET_cat"]
      Bounds = row["Bound"]
      bounds[age_cat] = bounds.get(age_cat,{})
      bounds[age_cat][ET_cat] = bounds[age_cat].get(ET_cat,{})
      bounds[age_cat][ET_cat][Bounds] = row[calculateRespiratorySupportScore.RSV_order]
    calculateRespiratorySupportScore.RSV_bounds = bounds
  if "RST_bounds" not in calculateRespiratorySupportScore.__dict__:
    df = pd.read_csv("./config/RST_Bounds.tsv",sep='\t')
    bounds = {}
    for i,row in df.iterrows():
      print()
      RST = row["RST"]
      bounds[RST]={ "LB":row["LB"],
                    "UB":row["UB"]}
    calculateRespiratorySupportScore.RST_bounds = bounds
  if "weights" not in calculateRespiratorySupportScore.__dict__:
    df = pd.read_csv("./config/RSV_Weights.tsv",sep='\t')
    weights = {}
    for i,row in df.iterrows():
      RST = row["RST"]
      weights[RST] = row[calculateRespiratorySupportScore.RSV_order]
    calculateRespiratorySupportScore.weights = weights
  RST = record["RST"]
  age_cat = record["age_cat"]
  ET_cat = record["ET_cat"]
  LB = calculateRespiratorySupportScore.RSV_bounds[age_cat][ET_cat]["LB"]
  UB = calculateRespiratorySupportScore.RSV_bounds[age_cat][ET_cat]["UB"]
  RSVs = record[calculateRespiratorySupportScore.RSV_order].apply(lambda x: 0 if x=="" else float(x) )
  RSVs = pd.concat([UB,RSVs],axis=1).min(axis=1)
  RSVs = pd.concat([LB,RSVs],axis=1).max(axis=1)
  RSS = ((RSVs-LB)/(UB-LB)*calculateRespiratorySupportScore.weights[RST]).sum() * \
        (calculateRespiratorySupportScore.RST_bounds[RST]["UB"]-calculateRespiratorySupportScore.RST_bounds[RST]["LB"]) + \
        calculateRespiratorySupportScore.RST_bounds[RST]["LB"]
  return RSS


if __name__ == "__main__":
  jw_dob = 1477235471
  df = pd.read_csv( "./output/pivoted.WithRST.tsv",
                    sep='\t',
                    keep_default_na=False)
  df = fillMeasurements(df)
  df["age_sec"] = df["VALID_FROM_DT_TM"].apply(lambda x: time.mktime(time.strptime(x,"%Y-%m-%d %H:%M:%S")))\
                                        .apply(lambda x: x-jw_dob)
  df["age_cat"] = df["age_sec"].apply(calculateAgeCategory)
  df["ET_cat"] = df["Airway Device Size"].apply(calculateETCategory)
  df["RSS"] = df.apply(calculateRespiratorySupportScore,axis=1)
   
  df.to_csv("./output/pivoted.WithRSS.tsv",
            sep='\t',
            index=False)
