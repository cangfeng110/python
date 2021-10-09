#!/bin/bash

main()
{
    log_path=$(readlink -f $1)
    run_path=$(readlink -f $2)
    curr_path=$(pwd)
    echo $log_path

    rm $log_path/*~

    for item in $(ls $log_path); do
        if [ -d $log_path/$item ]; then
            echo "Evaluating junction traj for "$item
            bash junction_traj_eval_multi_cases.sh $log_path/$item $run_path
        fi
    done
}

main $1 $2
