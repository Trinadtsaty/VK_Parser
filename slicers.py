import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

def get_name(group_info):
    try: 
        return group_info.get("NAME","") if group_info != "NaN" else ""
    except:
        return ""

def add_intersection_and_any(input_path, list_of_groups, output_path = ''):
    #read data
    players_with_groups = pd.read_json(input_path)

    def is_in_intersection(groups, list_of_groups = list_of_groups):
        return set(groups).intersection(set(list_of_groups)) == set(list_of_groups)

    def is_in_anyone(groups, list_of_groups = list_of_groups):
            return set(groups).intersection(set(list_of_groups)) != set({})

    #get names of groups
    players_with_groups['GROUPS_names'] = players_with_groups['GROUPS'].\
        apply(lambda lst: [get_name(x) for x in lst] )

    #add new columns to dataframe
    players_with_groups['intersection'] = players_with_groups['GROUPS_names'].apply(is_in_intersection)
    players_with_groups['is_in_any'] = players_with_groups['GROUPS_names'].apply(is_in_anyone)

    if output_path:
         players_with_groups.to_json(output_path)

    return players_with_groups

def apply_slicer(data, slicer = "intersection"): #slicer in ("intersection", "any")
     
    if slicer == "intersection":
        return data[data["intersection"] == True]
     
    if slicer == "any":
        return data[data["is_in_any"] == True] 

    else: 
        return None 

