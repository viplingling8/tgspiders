# -*- coding: utf-8 -*-

from tgspiders.crawler.base import post_data, get_data
from tgspiders.lib.err_util import retry
from tgspiders.lib.log import Log
import requests
import random
import json


class PickRealtimeWeather(object):
    def __init__(self):
        super(PickRealtimeWeather, self).__init__()
        self.log = Log()
        self.city_codes = self.__get_city_names__()
        self.session = requests.Session()
        self.appkey = ['0baf7dc59d774183920bab373ebd43d7', 'a0ae5d3490eb43498305a06245eba763',
                       'e1909f6b9ce046739ab2784bba806021', '1c3b75e46bd74d1d82e555b6c554c80e',
                       'f8679afda33d420eaa2a49d61022774d', '50679a30cb2948b4b6415d93179ff105',
                       '6cf5bbd2a6c24562b95a205c92b7fa37']

    def __get_city_names__(self):
        res = get_data('tb_city/listAll')
        new_list = json.loads(res)
        new_dict = {}

        for items in new_list:
            if items['isCrawler']:
                cityId = items['cityId']
                cityName = items['cityName']
                new_dict[cityId] = cityName
        return new_dict

    @retry
    def crawl_data(self, city_code):
        r = self.session.get('https://free-api.heweather.com/s6/weather/' \
                             'now?key=%s&location=%s' % (random.choice(self.appkey), city_code))

        if r.ok:
            data = r.json()

            if data['HeWeather6'][0]['status'] == 'ok':
                return (data['HeWeather6'][0]['now']['tmp'], data['HeWeather6'][0]['update']['loc'],
                        data['HeWeather6'][0]['now']['cond_txt'])
            elif data['HeWeather6'][0]['status'] == 'no more requests':
                return self.crawl_data(city_code)
            else:
                self.log.logger.info('错误状态----------->%s' % data['HeWeather6'][0]['status'])
                return None

    @retry
    def crawl(self):
        res = list()

        for city_code, city_name in self.city_codes.items():
            self.log.logger.info('开始获取%s天气数据' % city_name)
            data = self.crawl_data(city_code)

            if data:
                con = dict()
                con['cityCode'] = city_code
                con['cityName'] = city_name
                con['datetime'] = data[1]
                con['temperature'] = data[0]
                con['cond'] = data[2]
                con['windDirection'] = None,
                con['windSpeed'] = None
                self.log.logger.info('获取%s天气最新更新时间为%s' % (city_name, data[1]))
                res.append(con)
        if res:
            self.log.logger.info('开始存储实时天气数据')
            r = post_data('realtimeweather/createBatch', data=res)
            if r:
                self.log.logger.info('完成存储实时天气数据')


if __name__ == '__main__':
    prw = PickRealtimeWeather()
    prw.crawl()
