import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, Future

from proxypool_thread.log import Log
from proxypool_thread.setting import *


class Task:
    def __init__(self, fun, *args, **kw):
        self.fun = fun
        self.args = args
        self.kw = kw
        self.name = fun.__str__()

    def run(self):
        if self.args:
            if self.kw:
                self.fun(*self.args, **self.kw)
            else:
                self.fun(*self.args)
        else:
            self.fun()


class Factory:
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            org = super(Factory, cls)
            cls._instance = org.__new__(cls, *args, **kw)
            cls._instance.task = []
            cls._instance.worker = []
            cls._instance._active_working = {"getter": 0, "tester": 0, "Scheduler": 0}
            cls._instance.web_worker = Future()
            cls._instance._pool = ThreadPoolExecutor(max_workers=CONCURRENT)
            cls._instance.pool_status = True
            cls._instance.mutex = threading.Lock()
        return cls._instance
    # 活动中的计数
    def _minus_active(self, name):
        with self.mutex:
            if "Crawler" in name:
                self._active_working["getter"] -= 1
            elif "test_single_proxy" in name:
                self._active_working["tester"] -= 1
            else:
                self._active_working["Scheduler"] -= 1

    def _plus_active(self, name):
        if "Crawler" in name:
            self._active_working["getter"] += 1
        elif "test_single_proxy" in name:
            self._active_working["tester"] += 1
        else:
            self._active_working["Scheduler"] += 1

    def _sleep(self, worker_id):
        if type(worker_id) == float:
            pass
        Log.debug(f"工人{worker_id}号，沉睡")
        time.sleep(WORKSLEEP)

    def _create_worker(self):
        self.worker = [self._pool.submit(self._working, i) for i in range(CONCURRENT)]

    def _working(self, worker_id):
        while self.pool_status:
            if not self.task:
                self._sleep(worker_id)
                continue
            t = self._get()
            try:
                t.run()
            except Exception:
                Log.error(f"工人工作异常: {traceback.format_exc()}")
            finally:
                self._minus_active(t.name)
        Log.debug(f"工人{worker_id}雇佣结束")

    def _get(self) -> (Task, None):
        with self.mutex:
            try:
                return self.task.pop()
            except IndexError:
                return None

    def add(self, fun, *args, **kwargs):
        with self.mutex:
            t = Task(fun, *args, **kwargs)
            self._plus_active(t.name)
            self.task.append(t)

    def get_active(self, name):
        with self.mutex:
            return self._active_working[name]

    # 单批次任务等待完成
    def wait(self, name):
        Log.info(f"{name} 等待本次执行完毕")
        while self.get_active(name) > 0:
            time.sleep(EXCUTE_CYCLE / 2)
            # if "tester" == name:
            #     pass
        Log.info(f"{name} 结束等待 {self.get_active(name)}")

    def cencel(self):
        if self.pool_status:
            self.pool_status = False
            self.web_worker.cancel()
            for w in self.worker:
                w.cancel()

    def add_api(self, fun):
        self.web_worker = self._pool.submit(fun)

    def start(self):
        Log.debug("线程池启动，创建工人")
        self._create_worker()
        Log.debug("工人准备就绪")
        while self.pool_status:
            time.sleep(EXCUTE_CYCLE)
        Log.debug("线程池关闭")
        # 关闭池
        return self._pool.shutdown()


if __name__ == '__main__':
    f = Factory()
    f.start()
    print("done")
