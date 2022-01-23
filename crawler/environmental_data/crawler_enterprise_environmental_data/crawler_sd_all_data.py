# -*- coding: utf-8 -*-

from tgspiders.crawler.environmental_data.crawler_enterprise_environmental_data.base import Base
from tgspiders.lib.post_root import qy_decetion, get_qy_id_url_lasttime
from tgspiders.lib.float_util import float_cast
from tgspiders.lib.log import Log
from datetime import datetime
import calendar
import json
import math
import time


class SDEmissionPickerData(Base):
    def __init__(self):
        super(SDEmissionPickerData, self).__init__('http://121.28.49.84:8003/')
        self.province_id = 37000000
        self.log = Log()
        self.href = 'http://58.56.98.78:8405'
        self.city_href = {
            # '济南': 'http://119.164.252.34:8403',
            '青岛': 'http://219.147.6.195:8403',
            '淄博': 'http://60.210.111.130:8406',
            # '枣庄': 'http://218.56.152.39:8403',
            '东营': 'http://221.2.232.50:8401',
            '烟台': 'http://218.56.33.245:8403',
            '潍坊': 'http://122.4.213.20:8403',
            '济宁': 'http://60.211.254.236:8403',
            '泰安': 'http://220.193.65.234:8403',
            '威海': 'http://60.212.191.18:8408',
            '日照': 'http://219.146.185.5:8404',
            '莱芜': 'http://218.56.160.167:8403',
            '临沂': 'http://58.57.43.244:8414',
            '德州': 'http://222.133.11.150:8403',
            '聊城': 'http://222.175.25.10:8403',
            '滨州': 'http://222.134.12.94:8403',
            '菏泽': 'http://219.146.175.226:8403'}

    def get_all_qyinfo_by_provinceid(self, province_id, qy_style):
        list_qyinfo = []
        list_qy = get_qy_id_url_lasttime(self.province_id, 1)
        # print(list_qy)
        for k in list_qy:
            dev = {}
            if not k['monitortime']:
                k['monitortime'] = '2019-01-01 00:00:00'
            dev['qy_id'] = k['qyid']
            dev['qy_name'] = k['qyname']
            dev['qy_city'] = k['qycity']
            dev['qy_url'] = k['qyurl']
            list_qyinfo.append(dev)

        return list_qyinfo

    def pick_dev_data(self, qy_info, start_time, end_time, year, page, page_rows):
        entCode = qy_info['qy_id']
        cityName = qy_info['qy_city']
        ent_href = qy_info['qy_url'].replace('/Ent/', '/ND/')

        try:
            jsoncallback = 'jQuery11110043904820099857744_1482223108531'
            ent_html = self.http.session.get(self.city_href[cityName] + '/ajax/npublic/NData.ashx',
                                             headers={'Connection': 'keep-alive',
                                                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36',
                                                      'Accept': '*/*',
                                                      'Referer': ent_href,
                                                      'Accept-Encoding': 'gzip, deflate, sdch',
                                                      'Accept-Language': 'zh-CN,zh;q=0.8'},
                                             params={'Method': 'GetMonitorDataList',
                                                     'jsoncallback': jsoncallback,
                                                     'EntCode': entCode,
                                                     'subType': '2,3',
                                                     'subID': '',
                                                     'year': year,
                                                     'itemCode': '',
                                                     'dtStart': start_time,
                                                     'dtEnd': end_time,
                                                     'monitoring': '1',
                                                     'bReal': 'false',
                                                     'page': page,
                                                     'rows': page_rows,
                                                     '_': '1482223108532'},
                                             timeout=600)

            const = ent_html.text if ent_html.ok else None

            if const is None:
                return None

            const = const.replace(jsoncallback, '').replace('(', '').replace(')', '')
            dev_datas = json.loads(const)

            return dev_datas
        except:
            return None

    def insert_dev_datas(self, dev_datas, qy_id):
        dev_list = ['华电5-6号']

        nowStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        nowDate = self.parser.set_date(nowStr).set_time(nowStr).datetime

        if len(dev_datas) < 1:
            return

        for dev_data in dev_datas:
            dev_name = dev_data['Subname']

            if dev_name in dev_list:
                continue

            timeStr = dev_data['Ac005_datetime']
            timeDate = self.parser.set_date(timeStr).set_time(timeStr).datetime

            if timeDate > nowDate:
                continue

            res = dict({k: None for k in self.sql_type})
            res['province_id'] = self.province_id
            res['enterprise_id'] = qy_id
            res['monitor_point'] = dev_name
            res['monitor_time'] = str(timeDate)
            res['project_id'] = dev_data['Itemname']
            res['monitor_value'] = float_cast(dev_data['Ac005_value']) if dev_data['Ac005_value'] != '' else None
            res['standard_limit_value'] = float_cast(dev_data['Stander']) if dev_data['Stander'] != '' else None
            res['evaluation_criterion'] = dev_data['Typecode'] + ' ' + dev_data['Mfrequency']
            self.log.logger.info(res)
            qy_decetion(res)

    def get_months(self, start_date, end_date):
        start_year = start_date.strftime('%Y')
        end_year = end_date.strftime('%Y')
        years = int(end_year) - int(start_year)
        start_month = start_date.strftime('%m')
        end_month = end_date.strftime('%m')
        months = int(end_month) + 12 * years - int(start_month)

        return months

    def pick_all(self):
        self.log.logger.info('开始获取山东环保数据')
        qy_infos = self.get_all_qyinfo_by_provinceid(self.province_id, 1)
        page_rows = 500

        for qy_info in qy_infos:
            qy_id = qy_info['qy_id']
            last_update_time = self.get_last_update_time(self.province_id, qy_id)
            start_date = last_update_time.strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = self.parser.set_date(start_date).set_time('00:00:00').datetime
            end_date = self.parser.set_date(end_date).set_time('00:00:00').datetime
            month = self.get_months(start_date, end_date) + 1

            for i in range(0, month):
                start_time = start_date.strftime('%Y-%m-%d')
                m = int(start_date.strftime('%m'))
                y = int(start_date.strftime('%Y'))

                if i > 0:
                    m = m + 1
                    if m > 12:
                        y = int(start_date.strftime('%Y')) + int(m / 12)
                        m = m - 12 * int(m / 12)

                    start_time = str(y) + '-' + str(m) + '-01'
                    if m < 10:
                        start_time = str(y) + '-0' + str(m) + '-01'

                if i == month - 1:
                    end_time = end_date.strftime('%Y-%m-%d')
                else:
                    mdays = calendar.monthrange(y, m)[1]
                    end_time = start_time.split('-')[0] + '-' + start_time.split('-')[1] + '-' + str(mdays)

                year = start_time.split('-')[0]
                dev_datas = self.pick_dev_data(qy_info, start_time, end_time, year, '1', str(page_rows))
                start_date = self.parser.set_date(start_time).set_time('00:00:00').datetime

                if dev_datas is None:
                    continue

                self.insert_dev_datas(dev_datas['rows'], qy_id)
                pages = math.ceil(dev_datas['total'] / page_rows)

                if pages < 2:
                    continue

                for page in range(2, pages + 1):
                    dev_datas = self.pick_dev_data(qy_info, start_time, end_time, year, str(page), str(page_rows))

                    if dev_datas is not None:
                        self.insert_dev_datas(dev_datas['rows'], qy_id)


if __name__ == '__main__':
    t = time.time()
    sd = SDEmissionPickerData()
    sd.pick_all()
    print('time----------------->', time.time() - t)
