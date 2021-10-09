#!/bin/bash

main()
{
    if [ "$#" -lt 7 ]; then
        echo "Not enough arguments!"
        exit
    fi

    log_path=$(readlink -f $1)
    run_path=$(readlink -f $2)
    case_path=$(readlink -f $3)
    s_date=$4
    e_date=$5
    vehicle_name=$6
    scenario=$7
    curr_path=$(pwd)

    cd $log_path
    mkdir -p tmp_log
    cd tmp_log
    rm -r *

    cd $curr_path
    python3 loshu_data_download.py --sdate $s_date --edate $e_date \
            --vehicle-name $vehicle_name --output-path $log_path/tmp_log

    bash extract_scenario_cases_real_multi_logs.sh $log_path/tmp_log \
         $run_path $case_path $scenario

    mv $log_path/tmp_log/* $log_path
    rm -r $log_path/tmp_log/

    for dir in $(find $case_path -mindepth 1 -maxdepth 1 -type d); do
        bash serialization_multi_cases.sh $dir $run_path \
             $dir/map_files/ $dir/log_files/
    done
}

main $1 $2 $3 $4 $5 $6 $7
