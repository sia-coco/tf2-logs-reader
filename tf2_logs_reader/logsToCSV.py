#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.7
# Author :  - https://github.com/sia-coco
########################

# IMPORTS
import os
import json



# CUSTOM IMPORTS
import config as cfg


''' TO DO LIST
'''


''' NOTES
File to handle converting logs to csv lines for data science.
'''

####################################################
###################| CLASSES |######################
####################################################


####################################################
##################| FUNCTIONS |#####################
####################################################

# STRUCTURE CONVERSION
def flattenDict(d, parent_key='', sep='_'):
    """ Takes a nested dict and flattens it. Handles list values and converts 
    them into dicts according to rules. 

    INPUTS: 
            a dict
            a prefix for the naming
            separator for the naming

    OUTPUT:
            the flat dict

    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k

        if isinstance(v, dict):
            items.extend(flattenDict(v, new_key, sep=sep).items())

        elif isinstance(v, list):

            if k == "class_stats":
                v = listToDict(v, "type")
            elif k in ["rounds", "events", "killstreaks", "chat"]:
                v = listToDict(v, use_index=True)
            elif cfg.DEBUG_MODE:
                print(f" > WARNING: logsToCSV, flattenDict, key '{k}' unkown and needs to be added to the function")

            items.extend(flattenDict(v, new_key, sep=sep).items())
            
        else:
            items.append((new_key, v))

    return dict(items)

def listToDict(dict_list, name_field=None, use_index=False):
    """  Converts a list of dicts into a dict of dicts. It uses values of the sub dicts 
    as keys for these sub dicts or simply uses their index.

    INPUTS: 
            the list of dicts
            name of the key in sub dicts from which to use the value as a key for the sub dicts
                example: using key "class" in [{'class': 'soldier', ...}] 
                            gives {'soldier': {'class': 'soldier, ...}}
    OUTPUT:
    """ 

    new_dict = None

    if use_index:
        new_dict = {str(i):item for i, item in enumerate(dict_list)}

    elif name_field in dict_list[0]:
        new_dict = {item[name_field]:item for item in dict_list}

    elif cfg.DEBUG_MODE:
        print(f" > ERROR: in logsToCSV.py -> listToDict, name '{name_field}' isn't in the dict {dict_list[0]}")

    return new_dict

# PRE PROCESSING
def idsToClass(data):
    """  
    
    TODO

    INPUTS: 
    OUTPUT:
    """ 

    # Saves the amount of players named for each class
    class_counts = {}

    # TODO

    # For each id name an associated class

    # Call dictKeyRename for each player

    return data

def filterOffclassGames():
    """  If a game has too much offclass (variety, amout, time) it's not counted.

    TODO

    INPUTS: 
    OUTPUT:
    """ 
    pass
    
def dictKeyRename(iterable, old_key, new_key):
    """ Renames a key in a dict, recursively.

    INPUTS:
        an iterable
        old_key (string)
        new_key (string)

    OUTPUT:
        a dict with renamed keys
    """

    if isinstance(iterable, dict):

        for key in list(iterable.keys()):
            if key == old_key:
                iterable[new_key] = iterable.pop(old_key)
                if type(iterable[new_key]) in [dict, list]:
                    iterable[new_key] = dictKeyRename(iterable[new_key], old_key, new_key)

            elif type(iterable[key]) in [dict, list]:
                iterable[key] = dictKeyRename(iterable[key], old_key, new_key)

    elif isinstance(iterable, list):
        for item in iterable:
            item = dictKeyRename(item, old_key, new_key)

    return iterable


# LOGS TO CSV
def logToCSV(log_file, ids_to_class=False):
    """  Reads a log file and makes a csv file out of it.

    INPUTS: 
            name of the log file (str)
    OUTPUT:
    """ 

    with open(os.path.join(cfg.LOGS_DIR, log_file)) as json_file:

        # Converting json data into python dict
        dict_data = json.load(json_file)

        for key in cfg.TOREMOVE_FROM_CSV_TOPKEYS:
            if key in dict_data:
                del dict_data[key]

        if ids_to_class:
            dict_data = idsToClass(dict_data)


        flat = flattenDict(dict_data)


    return flat

####################################################
###################| CONSTANTS |####################
####################################################


####################################################
####################| PROGRAM |#####################
####################################################

if __name__ == '__main__':

    pass
    
    csv = logToCSV("2704480.json", ids_to_class=True)


    # print(csv)

    # with open("flat.json", "w") as test_file:
    #     test_file.write(json.dumps(csv))



    # with open(os.path.join(cfg.LOGS_DIR, "2704480.json")) as json_file:

    #     # Converting json data into python dict
    #     data = json.load(json_file)

    #     data = dictKeyRename(data, "[U:1:184338716]", "soldier1")

    # with open("test.json", "w") as test_file:
    #     test_file.write(json.dumps(data))