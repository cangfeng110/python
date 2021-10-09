#!/bin/bash

main()
{
    if [ "$#" -lt 4 ]; then
        echo "Not enough arguments!"
        exit
    fi

    log_path=$(readlink -f $1)
    run_path=$(readlink -f $2)
    case_path=$(readlink -f $3)
    scenario=$4
    curr_path=$(pwd)

    for item in $(ls $log_path); do
        if [[ -d $log_path/$item ]]; then
            echo "Extracting scenario_cases from "$log_path/$item
            bash extract_scenario_cases_replay_one_log.sh $log_path/$item \
                 $run_path $case_path $scenario
        fi
    done
}

main $1 $2 $3 $4
