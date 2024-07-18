import asyncio
import threading
import time

from tornado.websocket import websocket_connect

if __name__ == "__main__":
    def multi_conn():
        async def conn() -> None:
            ws = await asyncio.ensure_future(websocket_connect("ws://127.0.0.1:8006/trans"))
            for i in range(1000):
                now = time.time()
                asyncio.ensure_future(ws.write_message(b"hello"))
                print("send finished")
                msg = await ws.read_message()
                print(f"cost time: {int((time.time() - now) / 1000)} ms")
                print(f"recv {msg}")
                time.sleep(1)
            ws.close()

        asyncio.run(conn())


    threads = []
    for i in range(500):
        thread = threading.Thread(target=multi_conn)
        threads.append(thread)

    # 启动所有线程
    for thread in threads:
        thread.start()

    # 等待所有线程结束
    for thread in threads:
        thread.join()
