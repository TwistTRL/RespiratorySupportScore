#!/usr/bin/env python

ALL_RST = set(["RA","MASK","BB","NC","HFNC","CPAP","BIPAP","BVM","PSV","PCV","VCV","HFOV","HFJV"])    #CMV

def AA_MAPPING(x):
  if "mapping" not in AA_MAPPING.__dict__:
    AA_MAPPING.mapping = {
      "No compromise": ALL_RST,
      "Endotracheal tube": set(["PSV","PCV","VCV","HFOV","HFJV"]),                #CMV
      "Tracheostomy": set([ "RA","BB","NC","MASK",
                            "PSV","PCV","VCV","HFOV","HFJV"
                            ]),                                         #TODO       #CMV
      "Oropharyngeal airway": set(["PSV"]),                             #TODO
      }
  return AA_MAPPING.mapping.get(x,ALL_RST)

def ODDFIO2_MAPPING(x):
  if "mapping" not in ODDFIO2_MAPPING.__dict__:
    ODDFIO2_MAPPING.mapping = {
      "Ventilator": set(["BIPAP", "CPAP", "PSV", "PCV","VCV", "HFOV", "HFJV"]),   #CMV
      "None": set(["RA"]),
      "BiPAP": set(["BIPAP"]),
      "Blow-By": set(["BB"]),
      "CPAP": set(["CPAP"]),
      "High-flow nasal cannula": set(["HFNC"]),
      "Trach collar": ALL_RST,                                          #TODO
      "Face tent": set(["MASK"]),
      "Aerosol mask": set(["MASK"]),
      "Hand-bag mask": set(["BVM"]),
      "Hand-bag ETT": set(["BVM"]),
      "Hand-bag mask": set(["BVM"]),
    }
  return ODDFIO2_MAPPING.mapping.get(x,ALL_RST)

def ODDLMIN_MAPPING(x):
  if "mapping" not in ODDLMIN_MAPPING.__dict__:
    ODDLMIN_MAPPING.mapping = {
      "Nasal cannula": set(["NC"]),
      "None": set(["RA"]),
      "Simple mask": ALL_RST,                                           #TODO
      "Blow-By": set(["BB"]),
      "High-flow nasal cannula": set(["HFNC"]),
      "CPAP": set(["CPAP"]),
      "BiPAP": set(["BIPAP"]),
    }
  return ODDLMIN_MAPPING.mapping.get(x,ALL_RST)

def OS_MAPPING(x):
  if "mapping" not in OS_MAPPING.__dict__:
    OS_MAPPING.mapping = {
      "Room air": set(["RA"]),
      "Oxygen delivery device": set(["NC","BB","MASK","HFNC","CPAP","BIPAP","PSV","PCV","VCV","HFOV","HFJV"]),   #CMV
    }
  return OS_MAPPING.mapping.get(x,ALL_RST)

def VM_MAPPING(x):
  if "mapping" not in VM_MAPPING.__dict__:
    VM_MAPPING.mapping = {
    "PCV -SIMV + PSV": set(["PCV","HFJV"]),   #CMV
    "PSV": set(["PSV","HFJV"]),
    "BIPAP (S/T)": set(["BIPAP"]),
    "CPAP": set(["CPAP"]),
    "PRVC-SIMV": set(["VCV"]),
    "BiPAP": set(["BIPAP"]),
    "HFOV 3100-A": set(["HFOV"]),
    "VCV-SIMV + PSV": set(["VCV"]),   #CMV
    "PRVC": set(["VCV"]),   #CMV
    "Pressure - A/C": set(["PCV"]),   #CMV
    }
  return VM_MAPPING.mapping.get(x,ALL_RST)

def ETCO2_MAPPING(x):
  if x != "":
    return set(["PSV","PCV","VCV","BVM"])   #CMV
  return ALL_RST

def FIO2_MAPPING(x):
  if x != "":
    return set(["NC","MASK","HFNC","CPAP","BIPAP","PSV","BVM","PCV","VCV","HFOV","HFJV"])   #CMV
  return ALL_RST

def HFNC_MAPPING(x):
  if x != "":
    return set(["MASK","HFNC"])
  return ALL_RST

def CPAP_MAPPING(x):
  if x != "":
    return set(["CPAP"])
  return ALL_RST

def BIPAPEPAP_MAPPING(x):
  if x != "":
    return set(["CPAP","BIPAP"]);
  return ALL_RST

def BIPAPEPAP_MAPPING(x):
  if x != "":
    return set(["CPAP","BIPAP"])
  return ALL_RST

def BIPAPIPAP_MAPPING(x):
  if x != "":
    return set(["BIPAP"])
  return ALL_RST

def BIPAPRATE_MAPPING(x):
  if x != "":
    return set(["BIPAP"])
  return ALL_RST

def PEEP_MAPPING(x):
  if x != "":
    return set(["CPAP","BIPAP","PSV","PCV","VCV","HFJV"])   #CMV
  return ALL_RST

def PIP_MAPPING(x):
  if x != "":
    return set(["BIPAP","PSV","PCV","VCV","HFJV"])   #CMV
  return ALL_RST

def PS_MAPPING(x):
  if x != "":
    return set(["BIPAP","PSV","PCV","VCV","HFJV"])   #CMV
  return ALL_RST

def VR_MAPPING(x):
  if x != "":
    return set(["BIPAP","PCV","VCV","HFJV"])   #CMV
  return ALL_RST

def TV_MAPPING(x):
  if x != "":
    return set(["PCV","VCV"])    #CMV
  return ALL_RST

def TVS_MAPPING(x):
  if x != "":
    return set(["PSV","PCV","VCV"])           #CMV
  return ALL_RST

def TVM_MAPPING(x):
  if x != "":
    return set(["PSV","PCV","VCV"])           #CMV
  return ALL_RST

def HFJVPEEP_MAPPING(x):
  if x != "":
    return set(["HFJV"])
  return ALL_RST

def HFJVPIP_MAPPING(x):
  if x != "":
    return set(["HFJV"])
  return ALL_RST

def HFJVRATE_MAPPING(x):
  if x != "":
    return set(["HFJV"])
  return ALL_RST

def getRST(row):
  RSTs = ALL_RST.copy()
  for mapping,col in [
                      (AA_MAPPING,"Airway Assessment"),
                      (ODDFIO2_MAPPING,"Oxygen (FiO2) Delivery Device"),
                      (ODDLMIN_MAPPING,"Oxygen (L/min) Delivery Device"),
                      (OS_MAPPING,"Oxygen Source"),
                      (VM_MAPPING,"Ventilator Mode"),
                      (ETCO2_MAPPING,"End Tidal CO2"),
                      (FIO2_MAPPING,"Percent FiO2"),
                      (HFNC_MAPPING,"HFNC Flow"),
                      (CPAP_MAPPING,"Bubble Set CPAP"),
                      (BIPAPEPAP_MAPPING,"BiPAP EPAP Setting"),
                      (BIPAPRATE_MAPPING,"BiPAP IPAP Setting"),
                      (PEEP_MAPPING,"Apollo PEEP"),
                      (PIP_MAPPING,"PIP Calculation"),
                      (PS_MAPPING,"Pressure Support"),
                      (VR_MAPPING,"Ventilator Rate"),
                      (TV_MAPPING,"Tidal Volume"),
                      (TVS_MAPPING,"VT-Spontaneous (mL)"),
                      (TVM_MAPPING,"VT-Mandtory (mL)"),
                      (HFJVPEEP_MAPPING,"HFJV Monitored PEEP"),
                      (HFJVPIP_MAPPING,"HFJV PIP"),
                      (HFJVRATE_MAPPING,"HFJV Rate"),
                      ]:
    allowedRSTs = mapping(row.get(col,""))
    RSTs.intersection_update(allowedRSTs)
  return RSTs

def forwardFillRST(RSTs):
  curRST = None
  ffRST = []
  for i in RSTs:
    if curRST==None:
      if len(i)!=1 :
        ffRST.append(i)
      else:
        curRST = i
        ffRST.append(i)
    else:
      if len(i)==1:
        curRST = i;
        ffRST.append(i)
      else:
        if curRST.isdisjoint(i):
          curRST = None
          ffRST.append(i)
        else:
          ffRST.append(curRST)
  return ffRST

def backFillRST(RSTs):
  curRST = None
  bfRST = []
  for i in reversed(RSTs):
    if curRST==None:
      if len(i)!=1 :
        bfRST.append(i)
      else:
        curRST = i
        bfRST.append(i)
    else:
      if len(i)==1:
        curRST = i;
        bfRST.append(i)
      else:
        if curRST.isdisjoint(i):
          curRST = None
          bfRST.append(i)
        else:
          bfRST.append(curRST)
  return list(reversed(bfRST))

if __name__=="__main__":
  import pandas as pd
  df = pd.read_csv( "./output/pivoted.tsv",
                    sep='\t',
                    keep_default_na=False,
                    )
  df["RST_raw"] = df.apply(getRST,axis=1)
  df["RST_ForwardBackFill"] = backFillRST(forwardFillRST(df["RST_raw"]))
  df["RST"] = df["RST_ForwardBackFill"].apply(lambda x: list(x)[0] if len(x)==1 else None)
  df["RST"] = df["RST"].ffill()\
                        .iloc[::-1]\
                        .ffill()\
                        .iloc[::-1];
  df.to_csv("./output/pivoted.WithRST.tsv",
            sep='\t',
            index=False)


