#!/usr/bin/env python

import time
import pandas as pd

DATE_OF_BIRTH = 1540267200
FORMAT = "%Y-%m-%d %H:%M:%S"

def calculateAge(df):
  df["age_day"] = df["VALID_FROM_DT_TM"].apply(lambda x: (time.mkTime(time.strptime(x,FORMAT))-DATE_OF_BIRTH)/60/60/24 )
  return df

df = pd.read_csv("pivoted.tsv",sep='\t')
