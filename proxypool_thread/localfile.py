import threading
from random import choice

from proxypool_thread.log import Log
from proxypool_thread.setting import INITIAL_SCORE


class LocalDict(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            org = super(LocalDict, cls)
            cls._instance = org.__new__(cls, *args, **kw)
            cls._instance._proxy = dict()
            cls._instance.mutex = threading.Lock()
        return cls._instance

    # def __init__(self):
    #     self.proxys = dict()
    #     self.mutex = threading.Lock()

    def add(self, proxy, score=INITIAL_SCORE):
        with self.mutex:
            if proxy in self._proxy:
                return
            self._proxy[proxy] = score

    def get(self, proxy):
        return self._proxy.get(proxy)

    def delete(self, proxy):
        if self._proxy.get(proxy):
            try:
                self._proxy.pop(proxy)
            except Exception:
                pass

    def decrease(self, proxy, amount=-1):
        with self.mutex:
            try:
                self._proxy[proxy] += amount
            except Exception as e:
                print("ip 分数减少异常", e)

    def max(self):
        try:
            sort_proxy = sorted(self._proxy.items(), key=lambda x: x[1], reverse=True)
            target = choice(sort_proxy[:10])
            return target[0]
        except IndexError:
            target = list(self._proxy.keys())
            if not target:
                return ""
            return target[0]

    def clear(self):
        with self.mutex:
            try:
                useless = []
                for key, value in self._proxy.items():
                    if value <= 0:
                        useless.append(key)
                for i in useless:
                    Log.info(f"清理值为0的无效ip：{i}")
                    self._proxy.pop(i)
            except Exception as e:
                print("清理 ip 异常", e)

    def random(self):
        try:
            _proxy = list(self._proxy.keys())
            return choice(_proxy[:10])
        except IndexError:
            target = list(self._proxy.keys())
            if not target:
                return ""
            return target[0]

    def count(self):
        with self.mutex:
            return len(self._proxy)

    def batch(self, start, stop):
        with self.mutex:
            try:
                return list(self._proxy.keys())[start:stop]
            except IndexError:
                return []


if __name__ == '__main__':
    ld = LocalDict()
    s = {"aaa": 12, "bbb": 5, "ccc": 16, "ddd": 20}
    for k, v in s.items():
        ld.add(k, v)

    q = LocalDict()

    ld.decrease("aaa")
    ld.decrease("bbb", -10)
    print(ld.batch(1, 2))
    print(ld.count())
    print(ld.max())
    print(ld.random())
    print(ld.clear())
    print(ld.count())
    print()
