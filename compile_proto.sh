#!/bin/sh

main()
{
    if [ "$#" -lt 1 ]; then
        echo "Not enough arguments!"
        exit
    fi

    uos_dir=$(readlink -f $1)
    src_dir=$uos_dir/src/uos_local_planner/src/prediction/proto
    curr_path=$(pwd)

    cp $src_dir/*proto $curr_path/proto/
    protoc --proto_path=$curr_path/proto/ --python_out=$curr_path/core/ $curr_path/proto/*.proto
    cd $curr_path/core/ && sed -i -E 's/^import.*_pb2/from . \0/' *.py
}

main $1
