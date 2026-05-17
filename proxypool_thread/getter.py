import time
import traceback

from proxypool_thread.crawler import Crawler
from proxypool_thread.localfile import LocalDict
from proxypool_thread.log import Log
from proxypool_thread.setting import *
import sys

from proxypool_thread.factory import Factory


class Getter():
    def __init__(self):
        # self.redis = RedisClient()
        self.local = LocalDict()
        self.crawler = Crawler()
        self.factory = Factory()

    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        """
        if self.local.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False
    
    def run(self):
        t = set()
        count = self.local.count()
        if self.is_over_threshold():
            Log.info("Getter：此时容量已达上限，不获取ip")
            return
        Log.info(f'Getter：开始执行, 当前容量：{count}')
        for callback_label in range(self.crawler.__CrawlFuncCount__):
            try:
                callback = self.crawler.__CrawlFunc__[callback_label]
                # 获取代理
                t.add(self.factory.add(self.crawler.get_proxies, callback))
                sys.stdout.flush()
            except:
                traceback.print_exc()

        self.factory.wait(t)
        Log.info(f'Getter：执行结束, 获取前容量：{count}, 当前：{self.local.count()}')