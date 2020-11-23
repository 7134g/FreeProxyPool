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
    time.sleep(n)
    print("test22222222", n)
    # return

def test3(f):
    time.sleep(3)
    print("test333333333")
    # f.cencel()
    return


if __name__ == '__main__':
    f = Factory()
    f.add(test1, 'https://www.douban.com/')
    # for i in range(20):
    #     f.add(test1, 'https://www.baidu.com/')
    f.add(test2, 2)
    f.add(test3, f)
    f.wait()
    f.start()
    print("done")


