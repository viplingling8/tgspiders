# -*- coding: utf-8 -*-

from tgspiders.crawler.base import post_data, get_data
from tglibs.date_time_parser import DateTimeParser
from tgspiders.lib.http_util import HttpUtil
from tgspiders.lib.err_util import retry
# from tglibs.pinyin_util import to_pinyin
from tgspiders.lib.log import Log
from concurrent import futures
from datetime import datetime
import random
import json
import bs4
import re

MAX_WORKERS = 100


class PickWeather:
    def __init__(self):
        self.log = Log()
        # self.city_codes, self.city_names = self.__get_city_codes__()
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
        self.city_names = {'太原': '53772', '长治': '53882', '大同': '53487', '晋城': '53976', '晋中': '71115', '临汾': '53868',
                      '吕梁': '71037', '朔州': '53578', '忻州': '53674', '阳泉': '53782', '运城': '53959'}
        self.date_parse = DateTimeParser()
        self.http = HttpUtil('http://tianqi.2345.com/t/wea_history/js/')
        self.get_old_weather_url = 'http://tianqi.2345.com/t/wea_history/js/'
        self.get_feature_weather_url = 'https://way.jd.com/he/freeweather'
        self.jd_appkey = ['add552e5b50f71b8f53b8260632ac5e7', '7e95937eabebb1aabfc599acaa2724a4',
                          'de1b19c9d82ba2a231adc58fcdc943d6', 'c61198a130b122f81a3bd46ae4a4bfa0',
                          '5e35521455ec18c6ff869ef87fdc87f2']
        # self.data_res = list()

    def __get_city_codes__(self):
        res = get_data('tb_city/listAll')
        self.log.logger.info('获取城市编码完毕')
        new_list = json.loads(res)
        new_dict = {}
        names_dict = {}
        for items in new_list:
            if items['isCrawler']:
                cityCode = items['cityCode']
                cityName = items['cityName']
                new_dict[cityCode] = cityName
                names_dict[cityName] = items['cityId']
        return new_dict, names_dict

    def get_number(self, txt):
        """
        正则匹配，获取温度数据 -- 不包含单位℃
        """
        m = re.compile('(-?\d+)').search(txt)
        if m:
            return int(m.groups()[0])

    def get_his_weather_by_date(self, item, date):
        dt = date.split('-')
        url = self.get_old_weather_url + dt[0] + dt[1].zfill(2) + '/' + str(item) + '_' + dt[0] + dt[1].zfill(
            2) + '.js'

        try:
            r = self.http.session.get(url)

            if r.ok:
                self.pick_hist_weather(r.text)
            else:
                url = self.get_old_weather_url + str(item) + '_' + dt[0] + dt[1] + '.js'
                r = self.http.session.get(url)

                if r.ok:
                    self.pick_hist_weather(r.text)
        except:
            time.sleep(1)
            r = self.http.session.get(url)

            if r.ok:
                self.pick_hist_weather(r.text)

    def get_his_weather(self, items, date):
        workers = min(MAX_WORKERS, len(items) / 60)
        # self.get_his_weather_by_date('57796', date)
        # for item in items:
        #     self.get_his_weather_by_date(item, date)

        with futures.ThreadPoolExecutor(workers) as executor:
            for item in items:
                executor.submit(self.get_his_weather_by_date, item, date)

    def request_feature(self, item):
        return self.http.session.get(self.get_feature_weather_url,
                                     params={'city': item, 'appkey': random.choice(self.jd_appkey)})

    @retry
    def pick_hist_weather(self, txt):
        self.log.logger.info('获取历史天气')
        con = txt.split('=')[1].split(';')[0]
        res = eval(con, {key: key for key in re.findall(r"\b\w+\b", con)})
        li = list()
        for days in res['tqInfo']:
            if days:
                new_content = dict()
                try:
                    new_content['city'] = res['city']
                except Exception as e:
                    self.log.logger.info(e)
                if not self.get_city_code(new_content['city']):
                    self.log.logger.info('%s 查不到ciyt_id' % new_content['city'])
                    continue
                new_content['cityCode'] = self.get_city_code(new_content['city'])
                new_content['areaCode'] = self.city_codes[new_content['cityCode']][1]
                new_content['date'] = str(self.date_parse.set_date(days['ymd']).datetime)[:10]
                new_content['accurateMaxTemperature'] = int(self.get_number(days['bWendu']))
                new_content['accurateMinTemperature'] = int(self.get_number(days['yWendu']))
                new_content['accurateWindDirection'] = days['fengxiang']
                new_content['accurateWindSpeed'] =  days['fengli'][:-1]
                new_content['accurateWeatherStyle'] = days['tianqi']
                li.append(new_content)

        if li:
            self.log.logger.info(li)
            # self.data_res.append(new_content)
            post_data('weather/saveOrUpdate', data=li)

    @retry
    def get_2345_page(self, city_id):
        self.log.logger.info('获取 %s 天气预报' % self.city_codes[city_id][0])
        # city_pinyin = to_pinyin(self.city_codes[city_id])
        # if self.city_codes[city_id] == '莆田':
        #     city_pinyin = 'putian'
        # new_url = 'http://kan.2345.com/tq/%s/%s' % (city_pinyin, city_id)
        # print(new_url)
        # url = 'http://tianqi.2345.com/%s/%s.htm' % (city_pinyin, city_id)
        url = 'http://tianqi.2345.com/today-%s.htm' % city_id
        self.log.logger.info(url)
        r = self.http.session.get(url)
        if r.ok:
            soup = bs4.BeautifulSoup(r.text, 'html5lib')
            lis = soup.find('div', attrs={'class': 'seven-day'}).find_all('li')
            res = list()
            for li in lis:
                new_content = dict()
                new_content['city_name'] = self.city_codes[city_id][0]
                new_content['city_code'] = self.get_city_code(new_content['city'])
                new_content['area_id'] = self.city_codes[new_content['cityCode']][1]
                new_content['date'] = ('%s-%s' % (
                    datetime.now().year,
                    '-'.join(li.find('em').text.split('/')))).split()[0]
                _wd = li.find('span', attrs={'class': 'tem-show'}).text.split('~')
                new_content['max_temperature'] = int(_wd[1][:-1])
                new_content['min_temperature'] = int(_wd[0])
                new_content['wind_direction'] = li.find('span', attrs={'class': 'wind-name'}).text.split('风')[0]+'风'
                new_content['wind_speed'] = li.find('span', attrs={'class': 'wind-name'}).text.split('风')[-1][:-1]
                new_content['weather_style'] = li.find('i').text
                new_content['source'] = 'http://tianqi.2345.com/'
                res.append(new_content)
            if res:
                self.log.logger.info(res)
                post_data('weather/saveOrUpdate', data=res)

    def get_city_code(self, city_name):
        return self.city_names[city_name] if city_name in self.city_names else None

    def get_feature_weather_2345(self):
        workers = min(MAX_WORKERS, len(self.city_codes.keys()) / 60)
        with futures.ThreadPoolExecutor(workers) as executor:
            executor.map(self.get_2345_page, list(self.city_codes.keys()))

    def start(self):
        today = datetime.today().date()
        date = str(today).split('-')
        date = date[0] + '-' + date[1]
        self.get_feature_weather_2345()
        self.get_his_weather(self.city_codes.keys(), date)

    def re_start(self):
        # self.get_feature_weather_2345()
        # self.get_feature_weather(self.city_names)
        city_codes = ['50936', '54157', '54363', '60727', '71532', '70489', '50949', '60795']
        today = datetime.today().date()
        date = str(today).split('-')
        date = date[0] + '-' + date[1]

        for i in range(10, 11):
            for item in range(2019, today.year + 1):
                self.get_his_weather(city_codes, str(item) + '-' + str(i))

        # self.get_his_weather(self.city_codes.keys(), date)


def post_city():
    city_info = [{'cityCode': '50936', 'cityName': '白城', 'cityInit': 'B', 'isEmploy': False, 'province': '吉林',
                  'isCrawler': True, 'cityId': 'CN101060601'}]
    # weather/info
    post_data('tb_city/saveOrUpdate', city_info)


if __name__ == '__main__':
    # post_city()
    import time
    import pandas as pd

    # post_city()
    t = time.time()
    pw = PickWeather()

    pw.start()
    # print(pw.__get_city_codes__())
    # pw.re_start()
    # print('data_res--------->', pw.data_res)
    # pd.Series(pw.data_res).to_csv(r'D:\test.csv')
    # print(pw.city_names)
    print('----totle------->', time.time() - t)
