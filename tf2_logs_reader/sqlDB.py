#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.6
# Author :  - https://github.com/sia-coco
########################

# IMPORTS
import sys

# FILE IMPORTS

# Sub-modules


####################################################
############| LIBRARY ... |############
####################################################

""" TO DO LIST ✔✘
"""

""" PROBLEMS
"""

""" NOTES
"""

####################################################
###################| CLASSES |######################
####################################################


####################################################
##################| FUNCTIONS |#####################
####################################################

# SQL FUNCTIONS
def connectToSQL(db_file):
    """ Creates a database connection to the SQLite database
        specified.

    INPUTS:
            db_file (database file name)
    OUTPUT:
            Connection object or None
    """

    conn = None

    try:
        conn = sqlite3.connect(db_file)
        return conn

    except Error as e:
        print(e)

    return conn


def execSQL(conn, sql_line):
    """ creates a table from an sql statement.

    INPUTS:
            Connection object
            a "CREATE TABLE" SQL statement
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_line)
    except sqlite3.Error as e:
        print(e)


####################################################
##################| VARIABLES |#####################
####################################################


####################################################
###################| CONSTANTS |####################
####################################################


####################################################
####################| PROGRAM |#####################
####################################################

if __name__ == "__main__" :
    pass
    