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

    python3 extract_scenario_cases_real.py --log-path $log_path \
            --run-path $run_path --case-path $case_path --scenario $scenario
}

main $1 $2 $3 $4
