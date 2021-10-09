#!/bin/bash

main()
{
    case_path=$(readlink -f $1)
    run_path=$(readlink -f $2)
    map_path=$(readlink -f $3)
    config_path=$(readlink -f $4)
    curr_path=$(pwd)

    for dir in $(find $case_path -mindepth 1 -maxdepth 1 -type d); do
	echo -e 'Serializing '$dir'...\n'
	./serialization_one_case.sh $dir $run_path $map_path $config_path
    done

    echo 'All done.'
}

main $1 $2 $3 $4
