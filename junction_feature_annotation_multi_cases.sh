#!/bin/bash

main()
{
    case_path=$(readlink -f $1)
    curr_path=$(pwd)
    echo $case_path

    rm $case_path/*~

    for item in $(ls $case_path); do
        if [ -d $case_path/$item ]; then
            echo "Annotating for junction scenario case "$item

            rm $case_path/$item/*annotation*

            python3 junction_feature_annotation_one_case.py \
                    --case-path $case_path/$item
        fi
    done
}

main $1
