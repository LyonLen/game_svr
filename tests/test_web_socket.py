import asyncio

from tornado.websocket import websocket_connect

if __name__ == "__main__":

    async def conn() -> None:
        ws = await asyncio.ensure_future(websocket_connect("ws://127.0.0.1:8888/trans"))
        for i in range(100):
            asyncio.ensure_future(ws.write_message(b"hello"))
            print("send finished")
            msg = await ws.read_message()
            print(f"recv {msg}")
        ws.close()


    asyncio.run(conn())
