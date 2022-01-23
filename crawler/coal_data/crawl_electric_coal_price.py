# -*- coding: utf-8 -*-

from tglibs.date_time_parser import DateTimeParser
from tgspiders.crawler.base import post_data
from tgspiders.lib.err_util import retry
from datetime import datetime, timedelta
from tgspiders.lib.log import Log
from pyquery import PyQuery as pq
import requests
import re


class CrawlElectricCoalPrice:
    def __init__(self):
        self.log = Log()
        self.session = requests.Session()
        self.parser = DateTimeParser()
        self.base_url = 'http://www.imcec.cn/zgdm'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'www.imcec.cn',
            'Referer': 'http://www.imcec.cn/zgdm',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.36'
        }

    @retry
    def crawl_price(self, year):
        url = self.base_url + '_' + str(year)
        r = self.session.get(url, headers=self.headers)

        if r.ok:
            self.log.logger.info('开始取数')
            data = r.text.encode(r.encoding)
            tables = pq(data)('table table table table')
            pattern = re.compile('(?P<year>\d{4})年(?P<month>\d{1,2})月', re.IGNORECASE)
            res = list()

            for tb in tables:
                values = []
                for tr in pq(tb).items('tr'):
                    values.append(tr.text())
                res.append(values)

            for i in range(1, len(res)):
                con = dict()
                for j in range(len(res[i])):
                    if not j:
                        dt = list(re.findall(pattern, res[i][j])[0])
                        dt[1] = dt[1].zfill(2)
                        con['date'] = str(self.parser.set_date('%s-%s-01' % (dt[0], dt[1])).datetime)
                    else:
                        con['area'] = res[0][j]
                        con['value'] = res[i][j]
                    if 'value' in con and con['value']:
                        li = [con]
                        self.log.logger.info(li)
                        post_data('coal/price/electric/update-batch', data=li)
        else:
            self.log.logger.info('获取页面失败')

    def start(self):
        self.log.logger.info('爬取全国及分省电煤价格指数')
        now_year = datetime.now()
        for i in range(4):
            use_year = now_year - timedelta(days=i * 365)
            self.crawl_price(use_year.year)
        self.log.logger.info('爬取全国及分省电煤价格指数完毕')


if __name__ == '__main__':
    ec = CrawlElectricCoalPrice()
    ec.start()
