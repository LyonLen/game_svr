#!/usr/bin/bash

cd ../../../

SVR_NAME="$1_svr"
PID_FILE_DIR=./script/pids/

kill_and_wait_for_process_exit() {
    local pidKilled=$1
    # shellcheck disable=SC2155
    local begin=$(date +%s)
    local end
    kill $pidKilled &
    while kill -0 $pidKilled >/dev/null 2>&1; do
        echo "killing $pidKilled wait 1 more second.."
        sleep 0.5
        end=$(date +%s)
        if [ $((end - begin)) -gt 60 ]; then
            echo -e "\nTimeout"
            break
        fi
    done
}

echo "------stop server start------"
echo "stopping $SVR_NAME ..."

start_time=$(date +%s)
# shellcheck disable=SC2045
for PID_FILE in $(ls $PID_FILE_DIR); do
    PID_ABS_PATH=$PID_FILE_DIR$PID_FILE
    PID=$(cat $PID_FILE_DIR$PID_FILE)
    kill_and_wait_for_process_exit $PID && rm $PID_ABS_PATH
    echo "$SVR_NAME with pid: $PID stopped!!"
done

echo "check if flask all down"
ps -elf | grep "python -m svrs"

end_time=$(date +%s)
echo "cost time: $(expr $end_time - $start_time)s"
echo "------stop server end------"

cd -
exit 0