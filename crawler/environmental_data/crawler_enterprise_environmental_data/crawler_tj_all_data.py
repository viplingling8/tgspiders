# -*- coding: utf-8 -*-

from tgspiders.crawler.environmental_data.crawler_enterprise_environmental_data.base import Base
from tgspiders.lib.post_root import qy_decetion, get_qy_id_url_lasttime
from tgspiders.lib.float_util import float_cast
from datetime import datetime, timedelta
from tgspiders.lib.log import Log
import time
import requests


class TJEmissionPickerData(Base):
    def __init__(self):
        super(TJEmissionPickerData, self).__init__('http://zxjc.sthj.tj.gov.cn:8888/PollutionMonitor-tj/publish.do')
        self.province_id = 12000000
        self.log = Log()

    def insert_dev_datas(self, dev_datas, qy_id):
        for item in dev_datas:
            res = dict({k: None for k in self.sql_type})
            res['province_id'] = self.province_id
            res['enterprise_id'] = qy_id
            res['monitor_point'] = item['JCDMC']
            res['monitor_time'] = item['JCRQ']
            res['project_id'] = item['ZBMC']
            res['monitor_value'] = float_cast(item['ZSND'])
            res['standard_limit_value'] = float_cast(item['XZXZ'])
            res['evaluation_criterion'] = item['SFCB']
            self.log.logger.info(res)
            qy_decetion(res)

    def pick_all(self):
        self.log.logger.info('开始获取天津环保数据')
        qy_ids = self.get_all_qyid_by_qy_wrylx(self.province_id, 1)
        _year = datetime.now().year
        _month = datetime.now().month
        for item in qy_ids:
            r = requests.post('http://zxjc.sthj.tj.gov.cn:8888/PollutionMonitor-tj/publishZXJGlist.do',
                              params={'ID': item['qy_id'].split('-')[1]},
                              data={
                                  'JCRQ': '',
                                  'lx': 'FQ',
                                  'year': _year,
                                  'month': _month,
                                  'page': '1',
                                  'rows': '6000'
                              })
            if r.ok and r.json().get('total'):
                self.insert_dev_datas(r.json().get('rows'), item['qy_id'])


if __name__ == '__main__':
    t = time.time()
    tj = TJEmissionPickerData()
    tj.pick_all()

    print('time---------------->', time.time() - t)
