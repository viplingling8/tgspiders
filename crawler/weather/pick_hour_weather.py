# -*- coding: utf-8 -*-

import requests
import bs4
import json
# import pandas as pd
from tgspiders.lib.log import Log
from datetime import datetime, timedelta
from tgspiders.lib.err_util import retry
from tgspiders.crawler.base import post_data, get_data

# city_code = {'60795': '镇赉', '50949': '松原', '60793': '长岭'}
days = ['today', 'tomorrow', 'third', 'fourth', 'fifth']
base_url = 'http://tianqi.2345.com/'
result = list()


class PickHourWeather(object):
    def __init__(self):
        super(PickHourWeather, self).__init__()
        self.log = Log()
        # self.city_codes = self.__get_city_names__()
        self.city_codes = {
              '53772': ['太原', '140100'],
              '53882': ['长治', '140400'],
              '53487': ['大同', '140200'],
              '53976': ['晋城', '140500'],
              '71115': ['晋中', '140700'],
              '53868': ['临汾', '141000'],
              '71037': ['吕梁', '141100'],
              '53578': ['朔州', '140600'],
              '53674': ['忻州', '140900'],
              '53782': ['阳泉', '140300'],
              '53959': ['运城', '140800']
             }
        self.session = requests.Session()

    def __get_city_names__(self):
        res = get_data('tb_city/listAll')
        new_list = json.loads(res)
        new_dict = {}

        for items in new_list:
            print(items)
            if items['isCrawler']:
                new_dict[items['cityId']] = (items['cityName'], items['cityCode'])
        return new_dict

    @retry
    def crawl_data(self, city_info, city_code):
        days = ['today', 'tomorrow', 'third', 'fourth', 'fifth']
        result = list()
        for index, _day in enumerate(days):
            r = requests.get(base_url + _day + '-' + city_code + '.htm')
            _tmp_day = datetime.now() + timedelta(days=index)
            if r.ok:
                soup = bs4.BeautifulSoup(r.text, 'html5lib')
                lis = soup.find(id='js_hours24').find_all('li')
                temp_texts = soup.find_all('script')[-3].text.split(';')[0].split(' = ')[-1]
                temps = temp_texts.replace('[','').replace(']','').split(',')
                for i, _li in enumerate(lis):
                    con = dict()
                    _time = _li.find('em').text
                    if '/' in _time:
                        _tmp_day += timedelta(days=1)
                        _time = '00:00'
                    elif '现在' in _time:
                        _time = datetime.now().strftime('%H:00')
                    con['city_name'] = city_info[0]
                    con['city_code'] = city_code
                    con['area_id'] = city_info[1]
                    con['date_time'] = _tmp_day.strftime('%Y-%m-%d') + ' ' + _time
                    con['temperature'] = temps[i]
                    con['wind_direction'] = _li.find_all('b')[0].text
                    con['wind_speed'] = _li.find_all('b')[1].text[:-1]
                    con['weather_style'] = _li.find_all('a')[0]['title'].split(' ')[1]
                    con['cond'] = _li.find('span').text
                    con['source'] = 'http://tianqi.2345.com/'
                    # con['aqiInfo'] = None
                    # con['aqiLevel'] = None
                    # con['icon'] = None
                    result.append(con)
        if result:
            self.log.logger.info('开始存储小时天气数据')
            r = post_data('/realtimeweather/hour/batch/modification', data=result)
            if r:
                self.log.logger.info('完成存储小时天气数据')

    @retry
    def crawl(self):
        for city_code, city_name in self.city_codes.items():
            self.log.logger.info('开始获取%s天气数据:%s' % (city_name, city_code))
            self.crawl_data(city_name, city_code)


if __name__ == '__main__':
    prw = PickHourWeather()
    prw.crawl()
