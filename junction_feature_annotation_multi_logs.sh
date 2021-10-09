#!/bin/bash

main()
{
    log_path=$(readlink -f $1)
    curr_path=$(pwd)
    echo $log_path

    rm $log_path/*~

    for item in $(ls $log_path); do
        if [ -d $log_path/$item ]; then
            echo "Annotating for "$item
            bash junction_feature_annotation_multi_cases.sh $log_path/$item
        fi
    done
}

main $1
