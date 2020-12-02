import gc
import time
import traceback

from proxypool_thread.server import app
from proxypool_thread.log import Log
from proxypool_thread.getter import Getter
from proxypool_thread.factory import Factory
from proxypool_thread.tester import Tester
from proxypool_thread.setting import *


def schedule_tester():
    """
    定时测试代理
    """
    tester = Tester()
    while True:
        try:
            tester.run()
        except:
            tester = Tester()
            Log.error(f'Tester: 测试代理异常, {traceback.format_exc()}')
        finally:
            gc.collect()
            time.sleep(TESTER_CYCLE)

def schedule_getter():
    """
    定时获取代理
    """
    getter = Getter()
    while True:
        try:
            getter.run()
        except:
            getter = Getter()
            Log.error(f'getter： 抓取代理异常, {traceback.format_exc()}')
        finally:
            gc.collect()
            time.sleep(GETTER_CYCLE)

def schedule_api():
    """
    开启API
    """
    app.run(API_HOST, API_PORT)


class Scheduler:
    def run(self):
        factory = Factory()
        # factory.set_active_count([Getter, Tester])
        try:
            if TESTER_ENABLED:
                factory.add(schedule_tester)
            if GETTER_ENABLED:
                factory.add(schedule_getter)
            if API_ENABLED:
                factory.add(schedule_api)
            factory.start()
        finally:
            factory.stop()
            factory.shutdown()


