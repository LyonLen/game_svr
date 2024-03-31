#!/usr/bin/bash

SVR_NAME="conn_svr"

echo "$SVR_NAME starting..."
# TODO 临时测试
cd ../../../

cpu_num=$(grep -c "model name" /proc/cpuinfo)
let 'cpu_num /= 2'
local_ip=0.0.0.0
port=8000

mkdir -p ./script/pids/
mkdir -p ./script/logs/

for i in $(seq 1 $cpu_num); do
    PID_FILE=$SVR_NAME"_$i".pid
    LOG_FILE=$SVR_NAME"_$i".log

    let 'port += 1'
    echo $SVR_NAME"_$i listen at: " $local_ip":"$port
    nohup python -m svrs.$SVR_NAME.$SVR_NAME $port $local_ip >>./script/logs/$LOG_FILE 2>&1 &
    echo $! >./script/pids/$PID_FILE
    echo $SVR_NAME"_$i started!"
done

ps -elf | grep "python -m svrs.$SVR_NAME"

# 临时测试，跳回脚本目录
cd -
exit 0
