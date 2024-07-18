import asyncio
import sys
import time

from tornado.httpserver import HTTPServer
from tornado.netutil import bind_sockets
from tornado.web import Application
from tornado.websocket import WebSocketHandler, WebSocketClosedError, websocket_connect

from src.logging_self.base import init_logger
from src.svr_base import SvrBase


class ConnSvr(SvrBase):

    def on_init(self):
        self.web_svr_event = asyncio.Event()
        self.web_svr = None
        self.svr_name = "conn"

    def on_start(self):
        global logger
        logger = init_logger(self.get_instance_name(), **dict(self.conf["LOG"]))

        # TODO 数据库加载，有些标志是放在redis，要来判断版本号，开服状态

        # TODO 配置加载，一般conn_svr只有加载那种服务器列表、黑名单、白名单

        # 暂时不采用多进程启动
        # tornado.process.fork_processes(1)

        async def post_fork_main():
            sockets = []
            try:
                sockets = bind_sockets(int(sys.argv[1]), address=sys.argv[2], reuse_port=True)
                self.web_svr = HTTPServer(
                    Application(
                        [("/trans", ConnMsgHandler)],
                        websocket_ping_interval=50,  # 每50秒，向客户端发送一次ping包
                        websocket_ping_timeout=180  # 4次服务器ping不回pong，则主动断开长链接
                    )
                )
                self.web_svr.add_sockets(sockets)
                await self.web_svr_event.wait()
            finally:
                for socket in sockets:
                    socket.close()
                self.loop.stop()

        self.loop.create_task(post_fork_main())

    def on_stop(self):
        self.web_svr_event.set()
        logger.info(f"{self.get_instance_name()} stopped")


class ConnMsgHandler(WebSocketHandler):

    COUNT = 0
    MSG_NUM = 0
    LAST_REPORT_TIME = time.time()

    async def open(self):
        self.ws_client = await asyncio.ensure_future(websocket_connect("ws://127.0.0.1:8005/trans"))
        ConnMsgHandler.COUNT += 1
        logger.debug("ws connection opened")

    async def on_message(self, message):
        logger.debug(f"ws connection got one msg: {message}")
        resp_bytes = await self._test_run_transaction(message)
        try:
            await self.write_message(resp_bytes)
        except WebSocketClosedError:
            logger.warning("ws connection closed accidentally")
        finally:
            logger.debug(f"ConnMsgHandler.COUNT: {ConnMsgHandler.COUNT}")

    def on_close(self):
        ConnMsgHandler.COUNT -= 1
        self.ws_client.close()
        logger.debug("ws connection closed")

    async def _test_run_transaction(self, message: bytes) -> bytes:
        ConnMsgHandler.MSG_NUM += 1
        start = time.time()
        if start - ConnMsgHandler.LAST_REPORT_TIME >= 10:
            logger.info(f"ConnMsgHandler.COUNT: {ConnMsgHandler.COUNT} {ConnMsgHandler.MSG_NUM / (start - ConnMsgHandler.LAST_REPORT_TIME):.2f} qps")
            ConnMsgHandler.LAST_REPORT_TIME = start
            ConnMsgHandler.MSG_NUM = 0
        logger.debug(f"ws connection _test_run_transaction with {message}")
        asyncio.ensure_future(self.ws_client.write_message(b"hello"))
        got_msg_back = await self.ws_client.read_message()
        cost_ms = int((time.time() - start) * 1000)
        if cost_ms < 10:
            logger.debug(f"_test_run_transaction cost {cost_ms} ms")
        else:
            logger.warning(f"_test_run_transaction cost {cost_ms} ms")
        return got_msg_back


if __name__ == "__main__":
    ConnSvr(svr_name="conn").start()
