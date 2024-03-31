#!/usr/bin/env bash

. ../base.sh

# TODO 以后如果有多svr、多环境，这个要传入
SVR_NAME="conn"

CONDA_ENV_SHELL_DIR=$TRUNK_PATH"/tools/publish/conda_env"

if [ $CONDA_DEFAULT_ENV != "base" ]; then
    echo -e "$WARNING_HEADER $CONDA_DEFAULT_ENV 不是conda-base环境"
    echo "请切到conda-base环境:"
    echo "conda deactivate"
    exit 1
fi


if [ $# -lt 1 ]; then
    echo "Usage:"
    echo "基于conda-yml文件, 创建conda环境"
    echo "./create_conda_env.sh {环境: dev|test|uat|release} {版本(可选): v1_0_0}"
    echo "比如:"
    echo "指定dev环境, 根据tools/publish/base.sh的版本:"
    echo "./create_conda_env.sh dev"
    echo "指定dev环境, 自己控制版本:"
    echo "./create_conda_env.sh dev v1_0_0"
    exit 1
fi

ENV_NAME=$1
if [[ ${ENV_NAMES[*]}  =~ $ENV_NAME ]]; then
    echo -e "输入环境名:\n"$ENV_NAME
else
    echo -e "$WARNING_HEADER $ENV_NAME 不在 [${ENV_NAMES[*]}] 中"
    exit 1
fi

echo -e "git分支:\n"$(git branch --show-current)

if [ $# -lt 2 ]; then
    EXECUTE_VERSION=$VERSION
    echo -e "$WARNING_HEADER 没有输入版本号，读取环境变量 VERSION（tools/publish/base.sh）为:\n$VERSION"
else
    EXECUTE_VERSION=$2
fi

# 强制使用清华源
echo -e "$EXECUTE_SHELL_HEADER pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple"
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
echo -e "$EXECUTE_SHELL_HEADER pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn"
pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

# 强制覆盖conda源为清华源
cp $CONDA_ENV_SHELL_DIR"/condarc" ~/.condarc.txt.txt

# 更新环境
echo -e "$EXECUTE_SHELL_HEADER conda env update --file $CONDA_ENV_SHELL_DIR"/"$SVR_NAME"_app_"$ENV_NAME".yml" --name $SVR_NAME"_svr_"$ENV_NAME"_"$EXECUTE_VERSION"
conda env update --file $CONDA_ENV_SHELL_DIR"/"$SVR_NAME"_svr_"$ENV_NAME".yml" --name $SVR_NAME"_svr_"$ENV_NAME"_"$EXECUTE_VERSION
