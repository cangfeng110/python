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

replay()
{
    source ./encrypt_param.sh
    rm etc/*json
    rm data/*ucpf
    source ./set_env.sh

    echo "launch uos system..."
    ./launch_uos.sh &
    TAG=true
    start_time=$(date +%s)
    sleep 10

    while $TAG; do
	end_time=$(date +%s)
	cost_time=$((end_time-start_time))
	if [ "${cost_time}" -gt 100 ]; then
	    TAG=false
	    echo "Time out, force uos to stop..."
	    ./stop_uos.sh
	    break
	fi

        sleep 0.5
        if grep -q 'Replay the last frame.' data/log/uos_replay.log; then
	    TAG=false
	    echo "This is the end of replay, stop the uos..."
            ./stop_uos.sh
	    sleep 5
            break
        fi

    done
}

main()
{
    case_path=$(readlink -f $1)
    run_path=$(readlink -f $2)
    map_path=$(readlink -f $3)
    config_path=$(readlink -f $4)
    curr_path=$(pwd)
    echo $case_path

    rm $case_path/*~

    for file in $(ls $case_path | grep ucdf); do
        cd $run_path
        backup_files

        cd $curr_path
        python3 serialization_prepare.py --case-path $case_path \
                --ucdf-name $file --run-path $run_path --map-path $map_path \
                --config-path $config_path

        if [[ $? != 0 ]]; then
            continue
        fi

        cd $run_path
        replay

        cp data/test.ucpf $case_path/
        restore_files
    done
}

main $1 $2 $3 $4
