import json
import re
import traceback

from lxml import etree

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
            for proxy in eval("self.{}()".format(callback)):
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

    def crawl_daili66(self, page_count=10):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            # print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

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

    def crawl_mimvp(self):
        """
        米扑代理 https://proxy.mimvp.com/
        :return:
        """
        url_list = [
            'https://proxy.mimvp.com/freeopen?proxy=in_hp',
            'https://proxy.mimvp.com/freeopen?proxy=in_tp',
            'https://proxy.mimvp.com/freeopen?proxy=out_hp'
            'https://proxy.mimvp.com/freeopen?proxy=out_tp'
        ]
        port_img_map = {'DMxMjg': '3128', 'Dgw': '80', 'DgwODA': '8080',
                        'DgwOA': '808', 'DgwMDA': '8000', 'Dg4ODg': '8888',
                        'DgwODE': '8081', 'Dk5OTk': '9999'}
        for url in url_list:
            html = get_page(url)
            if not html:
                return
            html_tree = etree.HTML(html)
            for tr in html_tree.xpath(".//table[@class='mimvp-tbl free-proxylist-tbl']/tbody/tr"):
                try:
                    ip = ''.join(tr.xpath('./td[2]/text()'))
                    port_img = ''.join(tr.xpath('./td[3]/img/@src')).split("port=")[-1]
                    port = port_img_map.get(port_img[14:].replace('O0O', ''))
                    if "*" in ip:
                        continue
                    if port:
                        yield '%s:%s' % (ip, port)
                except Exception as e:
                    print(e)

    def crawl_kxdaili(self):
        """ 开心代理 """
        target_urls = ["http://www.kxdaili.com/dailiip.html", "http://www.kxdaili.com/dailiip/2/1.html"]
        for url in target_urls:
            html = get_page(url)
            if not html:
                return
            tree = etree.HTML(html)
            for tr in tree.xpath("//table[@class='active']//tr")[1:]:
                ip = "".join(tr.xpath('./td[1]/text()')).strip()
                port = "".join(tr.xpath('./td[2]/text()')).strip()
                yield "%s:%s" % (ip, port)

    def crawl_dieniao(self):
        """ 蝶鸟IP """
        url = "https://www.dieniao.com/FreeProxy.html"
        html = get_page(url)
        if not html:
            return
        tree = etree.HTML(html)
        for li in tree.xpath("//div[@class='free-main col-lg-12 col-md-12 col-sm-12 col-xs-12']/ul/li")[
                  1:]:
            ip = "".join(li.xpath('./span[1]/text()')).strip()
            port = "".join(li.xpath('./span[2]/text()')).strip()
            yield "%s:%s" % (ip, port)

    def crawl_proxy11(self):
        """ PROXY11 https://proxy11.com """
        urls = [
            "https://proxy11.com/api/demoweb/proxy.json?country=cn",
            "https://proxy11.com/api/demoweb/proxy.json?country=hk",
            "https://proxy11.com/api/demoweb/proxy.json?country=tw",
        ]

        for url in urls:
            try:
                html = get_page(url)
                if not html:
                    return
                resp_json = json.loads(html)
                for each in resp_json.get("data", []):
                    yield "%s:%s" % (each.get("ip", ""), each.get("port", ""))
            except Exception as e:
                print(e)

    def crawl_jiangxianli(self):
        """ 免费代理库 """
        for page in range(1, 5):
            url = 'http://ip.jiangxianli.com/?country=中国&page={}'.format(page)
            html = get_page(url)
            if not html:
                return
            tree = etree.HTML(html)
            for index, tr in enumerate(tree.xpath("//table//tr")):
                if index == 0:
                    continue
                yield ":".join(tr.xpath("./td/text()")[0:2]).strip()


if __name__ == '__main__':
    c = Crawler()
    for i in c.crawl_kxdaili():
        print(i)
