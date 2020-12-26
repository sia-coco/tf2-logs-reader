#!/bin/bash


#   Usage :
#   sh tf2-logs-reader.sh [action]


echo "|"
echo "|--------| TF2 LOGS READER |--------"
echo "|"


if [ $# -eq 0 ]
then

    echo ""
    echo "> Error : undefined action."
    echo "> Did you mean : "
    echo "  - sh tf2-logs-reader.sh setup ?"
    echo "  - sh tf2-logs-reader.sh test ?"
    echo "  - sh tf2-logs-reader.sh [command] ?"
    echo "  - sh tf2-logs-reader.sh --help ?"
    echo ""

	exit

elif [ $1 = "setup" ]
then

    echo "|  >  Setup"

    # shifts params
    shift 1

    python3 setup.py $*

	exit

elif [ $1 = "test" ]
then

	echo "|  >  Test"

    # shifts params
    shift 1
    
    python3 tf2_logs_reader/main.py $*

    exit

else

    echo "|  >  Main"
    
    python3 tf2_logs_reader/main.py $* 


	exit

fi
