#!/usr/bin/env bash

. base.sh

for file_path in $(find $TRUNK_PATH/proto/ -name "*.proto"); do
    file_dir_path=$(dirname $(readlink -f $file_path))
    echo -e $EXECUTE_SHELL_HEADER $PROTOC --python_out $file_dir_path/proto_py/ --pyi_out $file_dir_path/proto_py/ -I$file_dir_path $(readlink -f $file_path)
    $PROTOC --python_out $file_dir_path/proto_py/ --pyi_out $file_dir_path/proto_py/ -I$file_dir_path $(readlink -f $file_path)
done

git add $TRUNK_PATH/proto/proto_py/*.py $TRUNK_PATH/proto/proto_py/*.pyi -v
git commit $TRUNK_PATH/proto/proto_py/*.py $TRUNK_PATH/proto/proto_py/*.pyi -m "auto commit proto_py" -v
git push -v