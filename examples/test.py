import time

from proxypool_thread.factory import Factory
from proxypool_thread.utils import get_page
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test1(url):
    get_page(url)
    print(url)
    # return

def test2(n):
    t = set()
    time.sleep(n)
    print("test22222222", n)
    for i in range(10):
        t.add(f.add(test1, 'https://www.baidu.com/'))
    f.wait(t)


def test3():
    time.sleep(3)
    print("test333333333")
    f.transfer(10)
    return

def test4():
    time.sleep(10)
    print("test444444444")
    f.transfer(5)


if __name__ == '__main__':
    f = Factory()
    f.add(test2, 2)
    f.add(test3)
    f.add(test4)
    f.start()
    print("done")


