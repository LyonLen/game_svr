# 项目名称
PROJ_NAME="game_svr"
# 当前版本
VERSION="v0_0_1"
# 代码路径
TRUNK_PATH="$HOME/$PROJ_NAME"
# 运行路径
RUN_PATH="/data/app/$PROJ_NAME"
# protoc路径
PROTOC="$TRUNK_PATH/tools/publish/ext/bin/protoc"
# 环境名称枚举
ENV_NAMES=("dev" "test" "uat" "release")
# 执行shell输出绿色
EXECUTE_SHELL_HEADER="\033[32m[EXECUTE SHELL]\033[0m"
# 执行失败输出红色
WARNING_HEADER="\e[91m[WARNING]\e[39m"