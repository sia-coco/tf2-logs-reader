import os
import tf2_logs_reader.config as cfg

####################
# WORKSPACE CONFIG #
####################



###### LOGS RETRIEVER

# List of steamid64 from uploaders you trust.
TRUSTED_UPLOADERS = cfg.TRUSTED_UPLOADERS

# Range of player amount you consider acceptable for a 6s game.
MIN_MAX_6S = cfg.MIN_MAX_6S

# List of Capture Point maps you want to consider for 6s. Has to be the exact names.
CP_MAPS   = cfg.CP_MAPS
# List of King Of The Hill maps you want to consider for 6s. Has to be the exact names.
KOTH_MAPS = cfg.KOTH_MAPS
# List of 6s maps you want to consider, all gamemodes.
SIXIES_MAPS = CP_MAPS + KOTH_MAPS


###### LOGS TO CSV

# PRE
csv_rule_pre = [[[]], []] # Rule skeleton
CSV_KEY_REMOVAL_RULES_PRE = cfg.CSV_KEY_REMOVAL_RULES_PRE

# POST
csv_rule_post = [[[]], []]# Rule skeleton
CSV_KEY_REMOVAL_RULES_POST = cfg.CSV_KEY_REMOVAL_RULES_POST

CSV_MAINCLASSES = cfg.CSV_MAINCLASSES
CSV_OFFCLASS_BLACKLIST = cfg.CSV_OFFCLASS_BLACKLIST
CSV_OFFCLASS_LIMITS_CRITERIA = cfg.CSV_OFFCLASS_LIMITS_CRITERIA
CSV_OFFCLASS_QUOTAS_CRITERIA = cfg.CSV_OFFCLASS_QUOTAS_CRITERIA
CSV_TOTAL_OFFCLASS_LIMIT = cfg.CSV_TOTAL_OFFCLASS_LIMIT
CSV_TOTAL_OFFCLASS_QUOTA = cfg.CSV_TOTAL_OFFCLASS_QUOTA
CSV_OFFCLASS_CRITERIAS = {"offclass_blacklist": CSV_OFFCLASS_BLACKLIST,
                        "offclass_limits": CSV_OFFCLASS_LIMITS_CRITERIA,
                        "offclass_quotas": CSV_OFFCLASS_QUOTAS_CRITERIA, 
                        "total_offclass_limit": CSV_TOTAL_OFFCLASS_LIMIT,
                        "total_offclass_quota": CSV_TOTAL_OFFCLASS_QUOTA}

CSV_CLASSLIMIT_RANGES = cfg.CSV_CLASSLIMIT_RANGES
CSV_CLASSLIMIT_CRITERIAS = {"classlimit_ranges": CSV_CLASSLIMIT_RANGES}
