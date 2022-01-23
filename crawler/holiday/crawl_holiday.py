# -*- coding: utf-8 -*-

from tgspiders.crawler.base import post_data
from tgspiders.lib.log import Log
from datetime import datetime
import json


class HolidayData:
    def __init__(self):
        self.log = Log()

    def post_holiday_data(self):
        self.log.logger.info('开始获取节假日信息')

        with open('../../TXT/tb_holiday.txt', 'r', encoding='utf8') as f:
            datas = f.readlines()

            for data in datas:
                print(data)
                data = json.loads(data)
                post_list = list()
                post_dict = dict()
                _y, _m, _d = data['date'].split('-')
                post_dict['date'] = "%s-%s-%s" % (_y, str(_m).zfill(2), str(_d).zfill(2))
                # rs = datetime.strptime(data['holidayName'], '%Y-%m-%d')
                # print(rs)

                post_dict['holidayName'] = data['holidayName']

                if post_dict['holidayName']:
                    post_dict['holiday'] = True
                else:
                    post_dict['holiday'] = False

                post_list.append(post_dict)
                self.log.logger.info('%s是%s' % (post_dict['date'], post_dict['holidayName']))
                post_data('holiday/saveOrUpdate', data=post_list)

    def start(self):
        self.post_holiday_data()


if __name__ == "__main__":
    hd = HolidayData()
    hd.start()
