import time

# from proxypool.scheduler import Scheduler
from proxypool_thread.scheduler import Scheduler
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    try:
        s = Scheduler()
        s.run()
        time.sleep(1800)
    except Exception as e:
        print("main error: ", e)
        time.sleep(1800)
        main()


if __name__ == '__main__':
    main()
