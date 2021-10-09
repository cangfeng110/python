#!/bin/bash

main()
{
    case_path=$(readlink -f $1)
    run_path=$(readlink -f $2)
    curr_path=$(pwd)

    rm $case_path/*~

    for item in $(ls $case_path); do
        if [ -d $case_path/$item ]; then
            echo "Evaluating junction traj for "$item
            bash junction_traj_eval_one_case.sh \
                 $case_path/$item $run_path $case_path/map_files \
                 $case_path/log_files/uos_common.json
        fi
    done
}

main $1 $2
