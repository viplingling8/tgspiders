# -*- coding: utf-8 -*-

import time
import calendar
import requests
from datetime import datetime
from tglibs.float_util import float_cast
from tglibs.date_time_parser import DateTimeParser
from tgspiders.crawler.environmental_data.crawler_enterprise_environmental_data.base import Base
from tgspiders.lib.post_root import qy_decetion


class LNEmissionPickerData(Base):
    def __init__(self):
        super(LNEmissionPickerData, self).__init__('http://218.60.144.99:8087/')
        self.province_id = 21000000
        self.href = 'http://218.60.144.99:8088'
        self.session = requests.Session()

    def pick_dev_data(self, qy_id, start_time, end_time):
        try:
            res = self.session.get(self.href + '/web/jbippSelfMonReport/getHistoryData',
                                        params={'entId': qy_id,
                                                'startDate': start_time,
                                                'endDate': end_time,
                                                'pollutantType': '',
                                                'polluatntGuid': '',
                                                'monId': '',
                                                'isOnline': ''},
                                        timeout=600)
            return res.json().get('result') if res.ok else None
        except:
            return None

    def insert_dev_datas(self, dev_datas, qy_id):
        for item in dev_datas:
            res = dict({k: None for k in self.sql_type})
            res['province_id'] = self.province_id
            res['enterprise_id'] = qy_id
            res['monitor_point'] = item['MON_NAME']
            res['monitor_time'] = item['DATA_TIME']
            res['project_id'] = item['POLLUTANT_NAME']
            res['monitor_value'] = float_cast(item['AVG_ZS'].split('mg')[0])
            res['standard_limit_value'] = float_cast(item['STD_VALUE'].split('mg')[0])
            res['evaluation_criterion'] = item['IS_OK']
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
        qy_infos = self.get_all_qyid_by_qy_wrylx(self.province_id, 1)
        for qy_info in qy_infos:
            last_update_time = qy_info['monitortime']
            start_date = last_update_time.split()[0]
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = DateTimeParser().set_date(
                start_date).set_time('00:00:00').datetime
            end_date = DateTimeParser().set_date(
                end_date).set_time('00:00:00').datetime
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
                    end_time = start_time.split(
                        '-')[0] + '-' + start_time.split('-')[1] + '-' + str(
                        mdays)

                dev_datas = self.pick_dev_data(qy_info['qy_id'], start_time, end_time)
                start_date = DateTimeParser().set_date(
                    start_time).set_time('00:00:00').datetime

                if dev_datas is None:
                    continue
                self.insert_dev_datas(dev_datas, qy_info['qy_id'])


if __name__ == '__main__':
    t = time.time()
    ln = LNEmissionPickerData()
    ln.pick_all()
    print('time----------------->', time.time() - t)
