set PROTOC="D:\Users\linliang1\PycharmProjects\game_svr\tools\publish\ext\protoc-26.0-win64\bin\protoc.exe"
set PROJECT_PATH="D:\Users\linliang1\PycharmProjects\game_svr"

FOR %%i IN (%PROJECT_PATH%\proto\*.proto) DO  (
    %PROTOC% --python_out %PROJECT_PATH%\proto\proto_py\ --pyi_out %PROJECT_PATH%\proto\proto_py\ -I%PROJECT_PATH%\proto %%i
)