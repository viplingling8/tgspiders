# -*- coding: utf-8 -*-

from tgspiders.crawler.base import post_data
from tgspiders.lib.log import Log
import json


class DistrictData(object):
    def __init__(self):
        self.log = Log()

    def post_all_district_data(self):
        self.log.logger.info('开始获取所有地区的编码')
        with open('./TXT/tb_etl_city_code.txt', 'r', encoding='utf8') as f:
            datas = f.readlines()

            for data in datas:
                data = json.loads(data)

                post_list = []
                post_dict = {}
                post_dict['cityId'] = data['cityId']
                post_dict['cityEn'] = data['cityEn']
                post_dict['cityZh'] = data['cityZh']
                post_dict['country'] = data['country']
                post_dict['countryEn'] = data['countryEn']
                post_dict['countryZh'] = data['countryZh']
                post_dict['provinceEn'] = data['provinceEn']
                post_dict['provinceZh'] = data['provinceZh']
                post_dict['intoProvinceEn'] = data['intoProvinceEn']
                post_dict['intoProvinceZh'] = data['intoProvinceZh']
                post_dict['cityLongitude'] = data['cityLongitude']
                post_dict['cityLatitude'] = data['cityLatitude']

                post_list.append(post_dict)
                self.log.logger.info('%s的城市编码是%s' % (post_dict['cityZh'], post_dict['cityId']))
                post_data('city/saveOrUpdate', data=post_list)

    def post_district_data(self):
        self.log.logger.info('开始获取要爬取的地区的编码')
        with open('./TXT/tb_citycode.txt', 'r', encoding='utf8') as f:
            datas = f.readlines()

            for data in datas:
                data = json.loads(data)

                post_list = []
                post_dict = {}
                post_dict['cityCode'] = data['city_code']
                post_dict['cityName'] = data['city_name']
                post_dict['cityInit'] = data['city_init']
                post_dict['isEmploy'] = data['is_employ']
                post_dict['province'] = data['province']
                post_dict['isCrawler'] = data['is_crawler']
                post_dict['cityId'] = data['city_id']

                post_list.append(post_dict)
                self.log.logger.info('%s的城市编码是%s' % (post_dict['cityName'], post_dict['cityId']))
                post_data('tb_city/saveOrUpdate', data=post_list)

    def start(self):
        self.post_all_district_data()
        self.post_district_data()


if __name__ == "__main__":
    dd = DistrictData()
    dd.start()
