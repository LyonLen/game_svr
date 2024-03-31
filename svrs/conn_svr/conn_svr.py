import asyncio
import logging

import tornado
from tornado.httpserver import HTTPServer
from tornado.netutil import bind_sockets
from tornado.process import task_id
from tornado.web import Application
from tornado.websocket import WebSocketHandler, WebSocketClosedError

from src.logging_self.base import init_logger
from src.svr_base import SvrBase


class ConnSvr(SvrBase):

    def on_init(self):
        self.web_svr_event = asyncio.Event()
        self.web_svr = None

    def on_start(self):
        global logger
        logger = init_logger(self.get_instance_name(), "./logs/conn_svr/", log_level=logging.DEBUG)

        # TODO 数据库加载，有些标志是放在redis，要来判断版本号，开服状态

        # TODO 配置加载，一般conn_svr只有加载那种服务器列表、黑名单、白名单

        tornado.process.fork_processes(2)

        async def post_fork_main():
            sockets = bind_sockets(8888, reuse_port=True)
            self.web_svr = HTTPServer(
                Application(
                    [("/trans", ConnMsgHandler)],
                    websocket_ping_interval=50,  # 每50秒，向客户端发送一次ping包
                    websocket_ping_timeout=180  # 4次服务器ping不回pong，则主动断开长链接
                )
            )
            self.web_svr.add_sockets(sockets)
            await self.web_svr_event.wait()

        self.loop.create_task(post_fork_main())

    def on_stop(self):
        self.web_svr_event.set()
        logger.info(f"{self.get_instance_name()} stopped")


class ConnMsgHandler(WebSocketHandler):

    async def open(self):
        logger.debug("ws connection opened")

    async def on_message(self, message):
        logger.debug(f"ws connection got one msg: {message}")
        resp_bytes = await self._test_run_transaction(message)
        try:
            await self.write_message(resp_bytes)
        except WebSocketClosedError:
            logger.warning("ws connection closed accidentally")

    def on_close(self):
        logger.debug("ws connection closed")

    async def _test_run_transaction(self, message: bytes) -> bytes:
        logger.debug(f"ws connection _test_run_transaction with {message}")
        return b'suss'


if __name__ == "__main__":
    ConnSvr().start()