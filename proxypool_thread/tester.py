import threading
import requests
from requests.exceptions import *

from proxypool_thread.log import Log
from proxypool_thread.utils import base_headers
from proxypool_thread.localfile import LocalDict
from proxypool_thread.factory import Factory
from proxypool_thread.setting import *


class Tester(object):
    def __init__(self):
        self.local = LocalDict()
        self.factory = Factory()
        self.mutex = threading.Lock()
        self._minus_count = 0

    def _minus(self):
        with self.mutex:
            self._minus_count += 1

    def test_single_proxy(self, url, proxy):
        """
        测试单个代理
        :param proxy:
        :return:
        """
        proxies = {
            "http": "http://" + proxy,
        }
        try:
            response = requests.head(url, headers=base_headers, proxies=proxies, timeout=15, allow_redirects=False,
                                     verify=False)
            status_code = response.status_code
            if status_code in VALID_STATUS_CODES:
                Log.debug(f'Tester：代理可用 {proxy}')
                pass
            else:
                if status_code in FORBIDEN_STATUS_CODES:
                    self._minus()
                    self.local.decrease(proxy, -MAX_SCORE)
                else:
                    self.local.decrease(proxy)
                Log.error(f'Tester：请求响应码不合法 {status_code} IP {proxy}')
        except (ReadTimeout, HTTPError, ProxyError, ConnectionError):
            self._minus()
            self.local.decrease(proxy, -MAX_SCORE)
            Log.warning(f'Tester：无用ip，直接删掉， ip: {proxy}')
        except (TypeError, AttributeError) as e:
            self.local.decrease(proxy)
            Log.error(f'Tester：代理请求失败 {proxy} ERROR: {e}')
    
    def run(self):
        """
        测试主函数
        :return:
        """
        t = set()
        count = self.local.count()
        if count == 0:
            Log.info("Tester：无代理")
            return
        Log.info(f'Tester：开始运行, 当前容量：{count}')
        try:
            stop = max(0, count)
            test_proxies = self.local.batch(0, stop)
            for proxy in test_proxies:
                for url in TEST_URLS:
                    t.add(self.factory.add(self.test_single_proxy, url, proxy))

            self.local.clear()

        except Exception as e:
            Log.error(f'Tester：发生错误 {e.args}')

        self.factory.wait(t)
        Log.info(f'Tester：执行结束, 测试前容量：{count}, 剩余：{count-self._minus_count}')
