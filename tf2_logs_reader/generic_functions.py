#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.7
# Author :  - https://github.com/sia-coco
########################

# IMPORTS

# CUSTOM IMPORTS


''' TO DO LIST
'''


''' NOTES
'''

####################################################
###################| CLASSES |######################
####################################################


####################################################
##################| FUNCTIONS |#####################
####################################################

def sumDicts(a, b):
    """ Adds the values of dict b to the ones of dict a. If a field of b doesn't exist in a, adds it.
    Modifies the given dict a.
    # TODO
    INPUTS:
    OUTPUT:
    """

    for field in b:
        if field in a:
            a[field] += b[field]
        else:
            a[field] = b[field]

    return a

def sumDictsOfDicts(a, b):
    """ #TODO

    INPUTS:
    OUTPUT:
    """

    for sub_dict in b:
        if sub_dict in a:
            a[sub_dict] = sumDicts(a[sub_dict], b[sub_dict])
        else:
            a[sub_dict] = b[sub_dict]

    return a

####################################################
###################| CONSTANTS |####################
####################################################


####################################################
####################| PROGRAM |#####################
####################################################

if __name__ == '__main__':

    pass