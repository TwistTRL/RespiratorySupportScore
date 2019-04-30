#!/usr/bin/env python

import pandas as pd

usedVariables = set([ "Airway Assessment","Oxygen (FiO2) Delivery Device","Oxygen (L/min) Delivery Device",
                      "Oxygen Source","Ventilator Mode","End Tidal CO2","Percent FiO2",
                      "Bubble Set CPAP","HFNC Flow",
                      "BiPAP EPAP Setting","BiPAP Rate",
                      "PIP Calculation","Pressure Support","Ventilator Rate",
                      "Tidal Volume","VT-Spontaneous (mL)","VT-Mandatory (mL)"
                      "HFJV Monitored PEEP","HFJV PIP","HFJV Rate",
                      "Airway Device Size"
                      ])

df = pd.read_csv( "./SampleData/rss_kim_HJ_1.csv",
                  usecols=["VALID_FROM_DT_TM","EVENT_CD_DESCR","RESULT_VAL"])
df = df.loc[(df["VALID_FROM_DT_TM"].notnull()) &
            (df["EVENT_CD_DESCR"].apply(lambda x: x in usedVariables))
            ]

df = pd.pivot_table(df,values="RESULT_VAL",index="VALID_FROM_DT_TM",columns="EVENT_CD_DESCR",aggfunc="last")

df.to_csv("./output/pivoted.tsv",sep='\t')
