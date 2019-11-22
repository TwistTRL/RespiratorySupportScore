# respiratory support score (RSS) and ECMO_VAD pipeline

RSS calculation was developed before I moved to airflow. The original plan was for me to provide python libraries, so Akash can build pipeline with them. This is why the RSS is not organized as airflow pipeline. Still, my RSS library encompass data collection, data transformation (calculation part), and data loading (into the database).

The extraction, transformation and loading script of RSS and ECMO are split into 3 repositories listed below. However, please consider adapting them to airflow pipeline.
https://github.com/TwistTRL/twist-data-collection
https://github.com/TwistTRL/twist-data-transformation
https://github.com/TwistTRL/twist-data-load

# ECMO_VAD
## Data collection
* script: https://github.com/TwistTRL/twist-data-collection/blob/master/twist_data_collection/ecmo_vad/__init__.py
* event mapping: https://github.com/TwistTRL/twist-data-collection/blob/master/twist_data_collection/ecmo_vad/data/v500_ecmo_vad_mapping.tsv
* required table:
  * P647S.CLINICAL_EVENT
  * DWTST.WEIGHTS
The ECMO VAD variables are collected directly from "P647S" (or V500) database, "clinical events" table as well as "weights" table in "DWTST" database. We then map the clinical events to our own variables, e.g. "ECMO Flow Measure (L/min)" and "ECMO Flow Set (L/min)" are mapped to "ECMO_FLOW" because they mean the same thing for us.

## Calculation
* script: https://github.com/TwistTRL/twist-data-transformation/blob/master/twist_data_transformation/ecmo_vad/__init__.py
* algorithm: see comments and code in the script:

## Loading into database
* script: https://github.com/TwistTRL/twist-data-load/blob/master/twist_data_load/ecmo_vad/__init__.py

# RSS 
## Data collection
* script: https://github.com/TwistTRL/twist-data-transformation/blob/master/twist_data_transformation/rsv/__init__.py
* event mapping: https://github.com/TwistTRL/twist-data-collection/blob/master/twist_data_collection/rsv/data/v500_rsv_mapping.tsv
* required table:
  * P647S.CLINICAL_EVENT
The RSS variables are collected directly from "P647S" (or V500) database, "clinical events" table. We then map the clinical events to our own variables according to the mapping.

## Calculation
* rst (type) calculation script: https://github.com/TwistTRL/twist-data-transformation/blob/master/twist_data_transformation/rsv/calculate_rst.py
* rss (score) calculation script: https://github.com/TwistTRL/twist-data-transformation/blob/master/twist_data_transformation/rsv/calculate_rss.py
* rsv_bounds: https://github.com/TwistTRL/twist-data-transformation/blob/master/twist_data_transformation/rsv/data/rsv_bounds.tsv
* rst_bounds: https://github.com/TwistTRL/twist-data-transformation/blob/master/twist_data_transformation/rsv/data/rst_bounds.tsv
* rsv_weights: https://github.com/TwistTRL/twist-data-transformation/blob/master/twist_data_transformation/rsv/data/rsv_weights.tsv
* algorithm:
We start by determining the respiratory support type (RST) because RST determines what weightings to use per "rsv_weights" and it also clips the final score to a certain range per "rst_bounds". To do this, we gradually narrow down the RST range. Given a data record, we start with all possible RSTs ("RA","MASK","BB","NC", etc.). Then we check each attribute of that data record.
For example, the code below says if "AIRWAY_ASSESSMENT" is "Endotracheal tube", then we can narrow down the RST to a subset of all possible RSTs.
```
def AA_MAPPING(x):
  if "mapping" not in AA_MAPPING.__dict__:
    AA_MAPPING.mapping = {
      "No compromise": ALL_RST,
      "Endotracheal tube": set(["PSV","PCV","VCV","HFOV","HFJV"]),
      "Tracheostomy": set([ "RA","BB","NC","MASK",
                            "PSV","PCV","VCV","HFOV","HFJV"
                            ]),
      "Oropharyngeal airway": set(["PSV"]),
      }
return AA_MAPPING.mapping.get(x,ALL_RST)
```
After accessing all attributes of a records, we normally end up with one RST and that will be the RST for the record. If it is not unique, then we use the previous (or subsequent) record's RST to help us determine the current RST (forward-fill and back-fill). 

When calculating RSS, all the respiratory support variables are clipped to a certain range (LB to UB) according to their age category and et category per "rsv_bounds".
Then, the clipped RSVs are scaled to 0-100 (let's call it RSV_score) according to their ratio within their range defined in "rsv_bounds". These RSV_score are then normalized by "rsv_weights" and summed into one score, (let's call it sum_score). This sum_score also ranges from 0-100, i.e. if all RSV_scores are 0, this sum_score is 0; if all RSV_scores are 100, this sum_score is 100. Then we scale the sum_score back to the range defined in "rst_bounds" such that a sum_score of 100 is mapped to the upper bound (UP)
according to "rst_bounds".
The follwoing code snippet from the script does pretty much all the above.
```
# twist-data-transformation/twist_data_transformation/rsv/calculate_rss.py : line 135
# Here, the RSV is already clipped
RSS = ((RSVs-LB)/(UB-LB)*calculate_respiratory_support_score.RSV_WEIGHTS[RST]).sum() * \
        (calculate_respiratory_support_score.RST_BOUNDS[RST]["UB"]-calculate_respiratory_support_score.RST_BOUNDS[RST]["LB"]) + \
calculate_respiratory_support_score.RST_BOUNDS[RST]["LB"]
```

For more detail, please consult the script.


## Loading into database
* script: https://github.com/TwistTRL/twist-data-load/blob/master/twist_data_load/ecmo_vad/__init__.py
