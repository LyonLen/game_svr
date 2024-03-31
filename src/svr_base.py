import asyncio
import configparser
import os.path
import signal
import time
from typing import final

_BASE_TIMER_SECONDS = 1.0


class SvrBase(object):

    @final
    def __init__(self, instance_id=0, svr_name="base"):
        self.instance_id = instance_id
        self.svr_name = svr_name
        self.loop = asyncio.new_event_loop()
        self._stopping = False
        self.on_init()
        self.conf = configparser.ConfigParser()
        self.conf.read(f'{os.path.dirname(os.path.dirname(__file__))}/conf/{svr_name}_svr.ini')

    @final
    def start(self):
        asyncio.set_event_loop(self.loop)
        self.loop.add_signal_handler(signal.SIGTERM, self.stop)
        self.loop.add_signal_handler(signal.SIGUSR1, self.stop)
        self.loop.add_signal_handler(signal.SIGUSR2, self.reload)
        self.loop.call_later(_BASE_TIMER_SECONDS, self.timer_callback)
        self.on_start()
        # 潜规则，通信模块虽已启动，因为还未await出让控制权，所以业务任务还未跑
        # 所以后加载配置表，这里简单认为不会有问题
        self.on_reload()
        self.loop.run_forever()

    @final
    def stop(self):
        self._stopping = True
        self.loop.stop()
        start_ms = int(time.time() * 1000)
        while self.loop.is_closed():
            self.loop.close()
        self.on_stop()
        from src.logging_self.base import logger
        logger.info(f"svr {self.get_instance_name()} stop cost {int(time.time() * 1000) - start_ms} ms")

    @final
    def reload(self):
        start_ms = int(time.time() * 1000)
        self.on_reload()
        from src.logging_self.base import logger
        logger.info(f"svr {self.get_instance_name()} reload cost {int(time.time() * 1000) - start_ms} ms")

    @final
    def timer_callback(self):
        # from src.logging_self.base import logger
        # logger.info(f"{self.get_instance_name()} timer %.1f seconds tick", _BASE_TIMER_SECONDS)
        if self._stopping:
            return
        self.on_tick()
        self.loop.call_later(_BASE_TIMER_SECONDS, self.timer_callback)

    @final
    def get_instance_name(self):
        return self.svr_name + "_" + str(self.instance_id)

    def on_tick(self):
        """
        Server系统级别的计时器触发的时机。建议子类继承后仅用于此种用途:
        1 系统资源监控（如cpu、内存、连接数等）
        2 程序资源监控（如事件循环task数量）
        3 业务统计（玩家数量等）

        切记不要在此时机处理重逻辑，重io、重计算。
        """
        pass

    def on_start(self):
        """
        Server的事件循环启动之前。一般会在这个时机做下列这些事情：
        1 日志模块初始化
        2 数据库模块初始化
        3 配置加载
        4 业务代码加载
        5 重启后恢复数据
        6 通信模块初始化
        """

    def on_stop(self):
        """
        Server收到停止信号后，准备停机。一般会在这个时机做下列这些事情：
        进程中有状态数据落地
        """
        pass

    def on_reload(self):
        """
        Server收到重载信号后。一般会在这个时机做下列这些事情：
        重新加载配置表、服务器配置。
        """
        pass

    def on_init(self):
        pass


if __name__ == "__main__":
    SvrBase().start()
