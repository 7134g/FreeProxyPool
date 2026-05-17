import re
import traceback

from proxypool_thread.localfile import LocalDict
from proxypool_thread.log import Log
from proxypool_thread.utils import get_page
from pyquery import PyQuery as pq


class ProxyMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(mcs, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        try:
            for proxy in getattr(self, callback)():
                Log.debug(f'getter：成功获取到代理: {proxy}')
                proxies.append(proxy)
        except:
            Log.error(f'getter：抓取代理异常，{traceback.format_exc()}')
            return
        self.save_proxies(proxies)

    def save_proxies(self, proxies):
        local = LocalDict()
        for proxy in proxies:
            local.add(proxy)

    def crawl_ip3366(self):
        for i in range(1, 10):
            start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(i)
            html = get_page(start_url)
            if html:
                find_tr = re.compile('<tr>(.*?)</tr>', re.S)
                trs = find_tr.findall(html)
                for s in range(1, len(trs)):
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(trs[s])
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(trs[s])
                    for address, port in zip(re_ip_address, re_port):
                        address_port = address + ':' + port
                        yield address_port.replace(' ', '')

    def crawl_89ip(self, page_count=6):
        """
        89免费代理
        """
        start_url = 'https://www.89ip.cn/index_{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('table tbody tr').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text().strip()
                    port = tr.find('td:nth-child(2)').text().strip()
                    if ip and port:
                        yield ':'.join([ip, port])

    def crawl_66daili(self, page_count=10):
        """
        66免费代理
        """
        start_url = 'http://www.66daili.com/?page={}'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            html = get_page(url)
            if html:
                ip_list = re.findall(r'<li[^>]*?min-width:\s*120px[^>]*?>([\d.]+)</li>', html)
                port_list = re.findall(r'<li[^>]*?min-width:\s*60px[^>]*?>(\d+)</li>', html)
                for ip, port in zip(ip_list, port_list):
                    yield ':'.join([ip, port])

    def crawl_proxyscrape(self):
        """
        ProxyScrape API - 返回纯文本 IP:PORT
        """
        url = 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all'
        html = get_page(url)
        if html:
            for line in html.strip().split('\n'):
                line = line.strip()
                if re.match(r'\d+\.\d+\.\d+\.\d+:\d+', line):
                    yield line

    def crawl_github_proxy(self):
        """
        GitHub 每日更新的免费代理列表
        """
        url = 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt'
        html = get_page(url)
        if html:
            for line in html.strip().split('\n'):
                line = line.strip()
                if re.match(r'\d+\.\d+\.\d+\.\d+:\d+', line):
                    yield line

    def crawl_zdaye(self):
        base_url = 'https://www.zdaye.com/dayProxy/{page}.html'
        head = {
            "Cookie": "_qddac=3-3-1.1.u7q9fs.khfmp63u; acw_tc=76b20f7016052337002376740e34e53c53751ff3dd45dc920c0e102e8298be; __51cke__=; Hm_lvt_80f407a85cf0bc32ab5f9cc91c15f88b=1605233700; __root_domain_v=.zdaye.com; _qddaz=QD.amc9vg.uv9mtn.khfmp5xx; _qdda=3-1.1; _qddab=3-u7q9fs.khfmp63u; _qddamta_2355087264=3-0; acw_sc__v2=5fadec2632d8f78e61f23f09232ed1c5c171b200; ASPSESSIONIDSGQQDQDB=HPEIIOOCNIFNIJAPKMGKBPIO; __tins__16949115=%7B%22sid%22%3A%201605233699770%2C%20%22vd%22%3A%204%2C%20%22expires%22%3A%201605236758401%7D; __51laig__=4; Hm_lpvt_80f407a85cf0bc32ab5f9cc91c15f88b=1605234959"}

        urls = [base_url.format(page=page) for page in range(1, 5)]

        for url in urls:
            proxy = {
                "http": "http://" + LocalDict().max(),
            }
            html = get_page(url, head, proxy)
            if html is None:
                continue
            doc = pq(html)
            for item in doc('#J_posts_list .thread_item div div p a').items():
                url_detail = 'https://www.zdaye.com' + item.attr('href')
                html_detail = get_page(url_detail, head, proxy)
                if html_detail is None:
                    break
                doc_detail = pq(html_detail)
                trs = doc_detail('.cont br').items()
                for tr in trs:
                    line = tr[0].tail
                    match = re.search(r'(\d+\.\d+\.\d+\.\d+):(\d+)', line)
                    if match:
                        host = match.group(1)
                        port = match.group(2)
                        yield ':'.join([host, port])


if __name__ == '__main__':
    c = Crawler()
    for i in c.crawl_zdaye():
        print(i)
