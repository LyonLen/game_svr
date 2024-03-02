import asyncio
import signal

from logging_self.base import logger

_BASE_TIMER_SECONDS = 1.0


class SvrBase(object):
    def __init__(self, instance_id=0, svr_name="base"):
        self.instance_id = instance_id
        self.svr_name = svr_name
        self._stopping = False
        self.loop = asyncio.new_event_loop()

    def start(self):
        asyncio.set_event_loop(self.loop)
        self.loop.call_later(_BASE_TIMER_SECONDS, self.timer_callback)
        self.loop.add_signal_handler(signal.SIGUSR1, self.stop)
        self.loop.add_signal_handler(signal.SIGUSR2, self.reload)
        self.on_start()
        self.loop.run_forever()

    def stop(self):
        self._stopping = True
        self.loop.stop()
        while self.loop.is_closed():
            self.loop.close()
        self.on_stop()

    def reload(self):
        logger.info(f"{self.get_instance_name()} reload")
        self.on_reload()

    def timer_callback(self):
        logger.info(f"{self.get_instance_name()} timer %.1f seconds tick", _BASE_TIMER_SECONDS)
        if self._stopping:
            return
        self.on_tick()
        self.loop.call_later(_BASE_TIMER_SECONDS, self.timer_callback)

    def get_instance_name(self):
        return self.svr_name + "_" + str(self.instance_id)

    def on_tick(self):
        pass

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def on_reload(self):
        pass


if __name__ == "__main__":
    SvrBase().start()
