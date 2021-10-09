#!/bin/bash

backup_files()
{
    if [ -f uos_config.json ]; then
        mv uos_config.json uos_config.json.bak
    fi

    for hmap in $(ls ./data/*hmap); do
        hmap_name=$(basename $hmap)
        if [ -f ./data/$hmap_name ]; then
            mv ./data/$hmap_name ./data/$hmap_name.bak
        fi
    done

    for rmap in $(ls ./data/*rmap); do
        rmap_name=$(basename $rmap)
        if [ -f ./data/$rmap_name ]; then
            mv ./data/$rmap_name ./data/$rmap_name.bak
        fi
    done
}

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

prediction_replay()
{
    source ./encrypt_param.sh
    rm etc/*json
    rm data/log/uos_local_planner.log
    source ./set_env.sh

    echo "start prediction replay..."
    ./bin/uos_prediction_replay
}

main()
{
    case_path=$(readlink -f $1)
    run_path=$(readlink -f $2)
    map_path=$(readlink -f $3)
    config_file=$(readlink -f $4)
    curr_path=$(pwd)
    echo $case_path

    rm $case_path/*~

    cd $run_path
    backup_files

    cd $curr_path
    python3 junction_traj_eval_prepare.py --case-path $case_path \
            --run-path $run_path --map-path $map_path --config $config_file

    if [[ $? != 0 ]]; then
        continue
    fi

    cd $run_path
    prediction_replay

    restore_files

    cd $curr_path
    python3 eval_trajectory_pred.py --log1 $run_path/data/log/uos_local_planner.log \
            --log2 $run_path/data/log/uos_local_planner.log --p $case_path
}

main $1 $2 $3 $4
