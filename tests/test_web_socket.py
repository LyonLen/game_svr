import asyncio
import time
import joblib
from joblib import delayed

from tornado.websocket import websocket_connect

if __name__ == "__main__":
    def multi_conn():
        async def conn() -> None:
            ws = await asyncio.ensure_future(websocket_connect("ws://127.0.0.1:8888/trans"))
            for i in range(10):
                asyncio.ensure_future(ws.write_message(b"hello"))
                print("send finished")
                msg = await ws.read_message()
                print(f"recv {msg}")
                time.sleep(0.1)
            ws.close()

        asyncio.run(conn())


    joblib.parallel.Parallel(n_jobs=-1, backend='threading')(
        delayed(multi_conn)()
        for _ in range(10000)
    )
