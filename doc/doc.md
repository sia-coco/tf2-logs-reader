# TF2 Logs Reader's Documentation

## Table of Contents

- [Files purposes](#files-purposes)


## Files purposes

### Summary

- [Main files](#main-files) :
    - [`setup.py`](#setup.py)
    - [`tf2-logs-reader.sh`](#tf2-logs-reader.sh)
    - [`tf2_logs_reader/config.py`](#tf2_logs_reader/config.py)
    - [`tf2_logs_reader/main.py`](#tf2_logs_reader/main.py)
    - [`tf2_logs_reader/logs-retriever.py`](#tf2_logs_reader/logs-retriever.py)
    - [`tf2_logs_reader/jsonDB.py`](#tf2_logs_reader/jsonDB.py)
    - [`tf2_logs_reader/sqlDB.py`](#tf2_logs_reader/sqlDB.py)

- [Class files](#class-files) :
    - [`tf2_logs_reader/Player.py`](#)
    - [`tf2_logs_reader/Match.py`](#)


### Main Files 

### `setup.py`
To be executed before the use of the Module. 

Contains the instructions to create the different folders and files necessary for the module to work properly.

It reads `tf2_logs_reader/config.py` to get the desired names of such folders and files.

### `tf2-logs-reader.sh`
The launch script of the module.

Module should be executed throught this script only.

### `tf2_logs_reader/config.py`
Contains all the configurations of the workspace and module. 

It is used through the whole program to determine where to search for and save data files.

It contains preferences constants for the data cleaning.

It contains SQL scripts for table creations for the SQL mode.

### `tf2_logs_reader/main.py`
Main python file of the module, the one executed by `tf2-logs-reader.sh`.

### `tf2_logs_reader/logs-retriever.py`
Contains all the functions to get logs from logs.tf

Filter logs using criterias, does rough cleaning to get rid of unusable/altered logs.

### `tf2_logs_reader/jsonDB.py`
JSON implementation of the module.

Stores and reads data in `.json` files.

### `tf2_logs_reader/sqlDB.py`
SQL implementation of the module.

Stores and reads data in a `sqlite3` database.


### Class files

### `tf2_logs_reader/Player.py`
Used by the JSON implementation.

Class that represents a player with his games and stats.

### `tf2_logs_reader/Match.py`
Used by the JSON implementation.

Class that represents a match with its stats.