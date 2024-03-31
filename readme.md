# 环境

## 硬件

8核 16G

### 操作系统--开发环境wsl

```shell
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=20.04
DISTRIB_CODENAME=focal
DISTRIB_DESCRIPTION="Ubuntu 20.04.6 LTS"
```

### 软件

```shell
git
conda 23.7.4
```

# 安装

```shell
# 拉取仓库
git clone https://github.com/LyonLen/game_svr.git

# 进入环境创建工具目录
cd tools/publish/conda_env/;

# 创建环境
./create_conda_env.sh dev
```

# 运行

```shell
# 启动conn_svr
nohup python -m svrs.conn_svr.conn_svr 8888 127.0.0.1 1>&2 >/dev/null &
# 启动zone_svr
nohup python -m svrs.zone_svr.zone_svr 9999 127.0.0.1 1>&2 > /dev/null &
# 运行测试脚本
cd tests;
python test_web_socket.py
```

# Client -> ConnSvr -> ZoneSvr 空架子性能测

## LOG: DEBUG

| client                       | conn_svr<br/>(%CPU %MEM) | conn_svr qps | zone_svr<br/>(%CPU %MEM) | 结论                  | 
|------------------------------|--------------------------|--------------|--------------------------|---------------------|
| c: 500 n: 500 * 1000 s: 1s   | 31.0 -> 44.6 0.4 -> 0.4  | 499.00 qps   | 20.8 -> 23.0 0.5 -> 0.5  | qps几乎和客户端一致         |
| c: 1000 n: 1000 * 1000 s: 1s | 67.0 -> 85.0 0.4 -> 0.4  | 950.79 qps   | 43.6 -> 47.0 0.3 -> 0.5  | qps有5%-10%损耗, 已达到极限 |

## LOG: INFO

| client                       | conn_svr<br/>(%CPU %MEM) | conn_svr qps | zone_svr<br/>(%CPU %MEM) | 结论                                  | 
|------------------------------|--------------------------|--------------|--------------------------|-------------------------------------|
| c: 500 n: 500 * 1000 s: 1s   | 18.8 -> 23.0  0.4 -> 0.4 | 499.65 qps   | 11.0 -> 15.0 0.2 -> 0.2  | qps几乎和客户端一致                         |
| c: 1000 n: 1000 * 1000 s: 1s | 29.0 -> 35.3  0.4 -> 0.4 | 895.73 qps   | 20.0 -> 28.4 0.3 -> 0.3  | 日志更少了，qps损耗更高。<br/>qps有10%损耗, 已达到极限 |

## c: 500 n: 500 * 1000 s: 1s 单事务耗时，较为少数超过10ms的请求

```
2024-04-01 00:45:39.519|pid(20153)|conn_0|MainThread|conn_svr.py:87|INFO|ConnMsgHandler.COUNT: 500 473.03 qps
2024-04-01 00:45:49.520|pid(20153)|conn_0|MainThread|conn_svr.py:87|INFO|ConnMsgHandler.COUNT: 500 491.67 qps
2024-04-01 00:45:59.523|pid(20153)|conn_0|MainThread|conn_svr.py:87|INFO|ConnMsgHandler.COUNT: 500 499.55 qps
2024-04-01 00:46:09.528|pid(20153)|conn_0|MainThread|conn_svr.py:87|INFO|ConnMsgHandler.COUNT: 500 499.37 qps
2024-04-01 00:46:19.529|pid(20153)|conn_0|MainThread|conn_svr.py:87|INFO|ConnMsgHandler.COUNT: 500 499.25 qps
2024-04-01 00:46:20.594|pid(20153)|conn_0|MainThread|conn_svr.py:97|WARNING|_test_run_transaction cost 19 ms
2024-04-01 00:46:20.744|pid(20153)|conn_0|MainThread|conn_svr.py:97|WARNING|_test_run_transaction cost 18 ms
2024-04-01 00:46:29.537|pid(20153)|conn_0|MainThread|conn_svr.py:87|INFO|ConnMsgHandler.COUNT: 500 498.89 qps
2024-04-01 00:46:39.539|pid(20153)|conn_0|MainThread|conn_svr.py:87|INFO|ConnMsgHandler.COUNT: 500 499.38 qps
2024-04-01 00:46:49.542|pid(20153)|conn_0|MainThread|conn_svr.py:87|INFO|ConnMsgHandler.COUNT: 500 499.66 qps
2024-04-01 00:46:59.553|pid(20153)|conn_0|MainThread|conn_svr.py:87|INFO|ConnMsgHandler.COUNT: 500 499.44 qps
2024-04-01 00:47:09.556|pid(20153)|conn_0|MainThread|conn_svr.py:87|INFO|ConnMsgHandler.COUNT: 500 499.47 qps
2024-04-01 00:47:10.464|pid(20153)|conn_0|MainThread|conn_svr.py:97|WARNING|_test_run_transaction cost 51 ms
```

## c: 1000 n: 1000 * 1000 s: 1s 单事务耗时，出现了大量的超过10ms的请求，从另一个角度解释了前后端对比，qps损耗的比例确实是较为真实的

```
2024-04-01 00:45:30.157|pid(20153)|conn_0|MainThread|conn_svr.py:97|WARNING|_test_run_transaction cost 61 ms
2024-04-01 00:45:30.178|pid(20153)|conn_0|MainThread|conn_svr.py:97|WARNING|_test_run_transaction cost 21 ms
2024-04-01 00:45:30.179|pid(20153)|conn_0|MainThread|conn_svr.py:97|WARNING|_test_run_transaction cost 22 ms
2024-04-01 00:45:30.181|pid(20153)|conn_0|MainThread|conn_svr.py:97|WARNING|_test_run_transaction cost 15 ms
2024-04-01 00:45:30.185|pid(20153)|conn_0|MainThread|conn_svr.py:97|WARNING|_test_run_transaction cost 12 ms
2024-04-01 00:45:30.194|pid(20153)|conn_0|MainThread|conn_svr.py:97|WARNING|_test_run_transaction cost 13 ms
2024-04-01 00:45:30.194|pid(20153)|conn_0|MainThread|conn_svr.py:97|WARNING|_test_run_transaction cost 13 ms
2024-04-01 00:45:30.212|pid(20153)|conn_0|MainThread|conn_svr.py:97|WARNING|_test_run_transaction cost 16 ms
2024-04-01 00:45:30.213|pid(20153)|conn_0|MainThread|conn_svr.py:97|WARNING|_test_run_transaction cost 16 ms
2024-04-01 00:45:30.217|pid(20153)|conn_0|MainThread|conn_svr.py:97|WARNING|_test_run_transaction cost 15 ms
2024-04-01 00:45:30.217|pid(20153)|conn_0|MainThread|conn_svr.py:97|WARNING|_test_run_transaction cost 14 ms
2024-04-01 00:45:30.217|pid(20153)|conn_0|MainThread|conn_svr.py:97|WARNING|_test_run_transaction cost 14 ms
2024-04-01 00:45:30.218|pid(20153)|conn_0|MainThread|conn_svr.py:97|WARNING|_test_run_transaction cost 14 ms
2024-04-01 00:45:30.218|pid(20153)|conn_0|MainThread|conn_svr.py:97|WARNING|_test_run_transaction cost 14 ms
2024-04-01 00:45:30.218|pid(20153)|conn_0|MainThread|conn_svr.py:97|WARNING|_test_run_transaction cost 14 ms
2024-04-01 00:45:30.218|pid(20153)|conn_0|MainThread|conn_svr.py:97|WARNING|_test_run_transaction cost 14 ms
```

# 结论

从空架子的测试结果来看，建议还是保持在500qps上下的压力。