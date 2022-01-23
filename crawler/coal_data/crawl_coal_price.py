# -*- coding: utf-8 -*-

from tgspiders.crawler.base import post_data
from datetime import datetime, timedelta
from tgspiders.lib.err_util import retry
from tgspiders.lib.log import Log
import requests
import time


class CrawlCoalPrice():
    def __init__(self):
        self.log = Log()
        self.session = requests.Session()
        self.now = datetime.now()
        self.date = self.now.date()
        self.fyg_places = {'秦皇岛': ['qhdmtjg','130300']}
        # self.fyg_places = {'曹妃甸': 'cfdmtjg', '天津港': 'tjgmtjg', '国投京唐港': 'gtjtgmtjg',
        #                    '京唐港': 'jtgmtjg', '黄骅港': 'hhgmtjg', '秦皇岛': 'qhdmtjg'}

    @retry
    def login(self):
        r = self.session.post('http://www.cqcoal.com/mars-web//hySpare/infoByZh', headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3011.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }, data={
            'fhyzh': 'togeek',
            'fhymm': 'tuji2016'
        })
        return r.ok

    @retry
    def crawl_fygmtjg(self, dt):
        '''
        发运港煤炭价格
        '''
        for key, place in self.fyg_places.items():
            r = self.session.post(
                'http://www.cqcoal.com/mars-web//fygmtjg/' + place[0],
                data={
                    'public_date': dt,
                    'area': '环渤海',
                    'place': key,
                    '_search': 'false',
                    'nd': str(int(time.time() * 1000)),
                    'rows': '-1',
                    'page': '1',
                    'sidx': '',
                    'sord': 'desc'
                })
            con = {}
            jsons = r.json()
            data = jsons['data']

            if r.ok and len(data) != 0:
                for i in data:
                    con['city_name'] = i['place']
                    con['area_id'] = place[1]
                    con['date'] = i['public_date']
                    con['coal_type'] = i['coal_type']
                    con['calorific_value'] = i['coal_power']
                    con['price'] = i['coal_max_price']
                    con['price_type'] = i['离岸价格']
                    con['source'] = i['秦皇岛煤炭网']
                    # con['sameRatio'] = i['ftb']
                    # con['linkRatio'] = i['fzdf']
                    # con['amplitude'] = i['fzd']
                    li = [con]
                    self.log.logger.info(li)
                    post_data('coal/price/departure/update-batch', data=li)
            else:
                self.log.logger.info('%s 或 %s不存在，请检查' % (key, place))

    def get_his_data(self, days):
        if self.login():
            self.log.logger.info('登录成功！')
            for day in range(days):
                his_time = self.date - timedelta(days=day)
                self.log.logger.info("日期: %s" % str(his_time))

                self.log.logger.info('爬取煤炭价格中心每日价格')
                self.crawl_fygmtjg(his_time)
        else:
            self.log.logger.info("登陆失败！")

    def start(self):
        if self.login():
            self.log.logger.info('登录成功！')
            self.log.logger.info("日期: %s" % str(self.date))

            self.log.logger.info('爬取煤炭价格中心每日价格')
            self.crawl_fygmtjg(self.date)
            self.log.logger.info('爬取完毕')
        else:
            self.log.logger.info("登陆失败！")


if __name__ == '__main__':
    ccp = CrawlCoalPrice()
    ccp.start()
    # ccp.get_his_data(300)
