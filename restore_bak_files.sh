#!/bin/bash

restore_files()
{
    if [ -f uos_config.json.bak ]; then
        mv uos_config.json.bak uos_config.json
    fi

    for hmap in $(ls ./data/*hmap.bak); do
        filename="${hmap%.*}"
        if [ -f $hmap ]; then
            mv $hmap $filename
        fi
    done

    for rmap in $(ls ./data/*rmap.bak); do
        filename="${rmap%.*}"
        if [ -f $rmap ]; then
            mv $rmap $filename
        fi
    done
}

main()
{
    if [ "$#" -lt 1 ]; then
        echo "Not enough arguments!"
        exit
    fi

    run_path=$(readlink -f $1)
    cd $run_path
    restore_files
}

main $1
