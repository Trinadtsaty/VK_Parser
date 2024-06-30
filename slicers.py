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


def apply_slicer(input_path, list_of_groups, slicer = "intersection", output_path = ''): #slicer in ("intersection", "any")

    assert slicer in ['intersection', 'any'], "не правильный слайсер, криворукая ты рожа"

    data = add_intersection_and_any(input_path, list_of_groups)
     
    if slicer == "intersection":
        filtred =  data[data["intersection"] == True]
     
    if slicer == "any":
        filtred =  data[data["is_in_any"] == True] 
    

    if output_path:
        filtred.to_json(output_path)

    return filtred


def new_into_data(old, new, id_field = "ID"):
    #принимает 2 датафрейма в одном формате (страый и новый), выдаёт 
    # выдаёт датафрем из тех, кого не было в страм, но тех, кто есть в новов
    old_ids = set(old[id_field].values())
    new_into = new[~new[id_field].isin(old_ids)]
    return new_into

