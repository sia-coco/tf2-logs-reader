#! /usr/bin/env python
#-*- coding: utf-8 -*-

########################
# Python 3.7
# Author :  - https://github.com/sia-coco
########################

# IMPORTS
import requests
from requests.exceptions import HTTPError

# CUSTOM IMPORTS
import config as cfg


''' TO DO LIST
'''


''' NOTES
'''

####################################################
###################| CLASSES |######################
####################################################

class LogsRetriever():
    """ 

    uploaders:
        76561197964045534 : TF2C
        76561197960497430 : serveme

    request_args = {"title":X, "uploader":Y, "player": Z, "limit": N, "offset": N}

    INPUTS:
            dict or arguments for the api request (see above)
    """

    def __init__(self, request_args):
        
        self.request_args = request_args

        # The response of logs.tf api for list of logs
        self.logs_tf_response = None

        # The list of logs we are going to work on
        self.log_list         = None


    def main(self):
        """ 
        """ 

        self.logs_tf_response = getLogsList(self.request_args)
        self.log_list = self.logs_tf_response["logs"]

        self.profilePlayersLogs()


    ###### CLEAN LOG LIST ######

    def cleanLogList(self, split_trusted=False):
        """  Cleans the log list according to given criterias
            
    
        INPUTS: 
                (option) keep logs from trusted uploaders
        """ 
        pass


    def splitLogsTrustedUntrusted(self):
        """  takes a list of logs and discriminates the ones from trusted 
        sources from the others.
    

        OUTPUT: 
                a list of "trusted" logs
                a list of the remaining logs
        """ 

        # The list of arguments can't specify uploaders. Since the goal is 
        #     to compare the whole group of uploaders with the trusted ones.
        if "uploader" in self.request_args:
            if self.request_args["uploader"] is not None:
                print(f" > ERROR : request_args{self.request_args} should not contain key 'uploader'.")
        
        # Getting every log id
        full_id_list = [k["id"] for k in self.log_list]
        

        ### Getting trusted sources logs
        trusted_uploaders_log_list = []
        trusted_uploaders_id_list = []

        for trusted_uploader in cfg.TRUSTED_UPLOADERS:

            # log list
            trusted_uploader_log_list = getLogsList({**self.request_args, **{"uploader": trusted_uploader}})["logs"]
            trusted_uploaders_log_list += trusted_uploader_log_list

            # log id list
            trusted_uploader_id_list = [k["id"] for k in trusted_uploader_log_list]
            trusted_uploaders_id_list += trusted_uploader_id_list

        ### Getting untrusted logs
        other_ids = set(full_id_list).symmetric_difference(set(trusted_uploaders_id_list))
        other_log_list = [log for log in self.log_list if log["id"] in other_ids]
        

        return (trusted_uploaders_log_list, other_log_list)
    

    ###### USER UTILITY/PRINTS ######

    def profilePlayersLogs(self):
        """  For each player, prints a recap of their logs.

        """ 
        
        result = obj.splitLogsTrustedUntrusted()

        print(f"total logs: {len(result[0])+len(result[1])}")
        print(f"trusted uploaders logs: {len(result[0])}")
        print(f"other logs: {len(result[1])}")



####################################################
##################| FUNCTIONS |#####################
####################################################

def getResponse(url, request_args):
    """ Gets the json response from a query.

    INPUTS:
            the url to query
            args for the query

    OUTPUT:
            json response
    """

    try:
        # Sends request
        response = requests.get(url, timeout=cfg.TIMEOUT_DELAY, params=request_args)

        # Check validity
        response.raise_for_status()


    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')

    except Exception as err:
        print(f'Other error occurred: {err}')

    else:
        return response.json()

def getLogsList(request_args):
        """ Retrieves json list of logs answer from logs.tf using search parameters.

        request_args = {"title":X, "uploader":Y, "player": Z, "limit": N, "offset": N}

        INPUTS:
                dict or arguments for the api request (see above)

        OUTPUT:
                the response of logs.tf api for list of logs
        """ 
        
        url = cfg.LOGS_LIST_URL

        return getResponse(url, request_args)


####################################################
###################| CONSTANTS |####################
####################################################


####################################################
####################| PROGRAM |#####################
####################################################

if __name__ == '__main__':

    # players = {
    #     "sia": "76561198377453187", 
    #     "kimmy": "76561198159697916", 
    #     "osborn": "76561198145652139", 
    #     "smiguel": "76561198056760624", 
    #     "snb": "76561198021205963",
    #     "houdini": "76561198020644759"}

    # players = {
    #     "pitts": "76561198091606463"}

    players = {
        "sia": "76561198377453187"}

    players = {
        "osb, kimmy": "76561198159697916,76561198145652139",
        "smi, kim, osb": "76561198159697916,76561198145652139,76561198056760624", 
        "smi, kim, osb, sia": "76561198159697916,76561198145652139,76561198056760624,76561198377453187", 
        "smi, kim, osb, sia, hud": "76561198159697916,76561198145652139,76561198056760624,76561198377453187,76561198020644759", 
        "smi, kim, osb, sia, hud, snb": "76561198159697916,76561198145652139,76561198056760624,76561198377453187,76561198020644759,76561198021205963",}

    for players_id in players: 

        print(players_id)

        args = {"title":None, "uploader":None, "player": players[players_id], "limit": 10000, "offset": None}
        obj = LogsRetriever(args)

        obj.main()

        print()




    