# -*- coding: utf-8 -*-

from tgspiders.crawler.environmental_data.crawler_all_enterprise.base import Base
from tgspiders.lib.post_root import qy_message
from tgspiders.lib.log import Log
from pyquery import PyQuery as pq
from datetime import datetime
import time
import json


class HAEmissionPicker(Base):
    def __init__(self):
        super(HAEmissionPicker, self).__init__('http://222.143.24.250:98/')
        self.log = Log()
        self.province_id = 41000000
        self.href = 'http://222.143.24.250:98/'

    def pick_enter_infos(self, year):
        try:
            res_html = self.http.session.get(self.href + "ashx/GetSiteInfo.ashx?type=1&regioncode=&enptype=2&enpname=&enpcode=&infoyear=" + year,
          headers={"Host": "222.143.24.250:98",
                    "Connection": "keep-alive",
                    "Accept": "*/*",
                    "X-Requested-With": "XMLHttpRequest",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36",
                    "Referer": "http://222.143.24.250:98/",
                    "Accept-Encoding": "gzip, deflate, sdch",
                    "Accept-Language": "zh-CN,zh;q=0.8"}, timeout=600)
            return res_html.text if res_html.ok else None
        except:
            return None

    def pick_enter_info(self, qy_url):
        try:
            enp_html = self.http.session.get(qy_url,
         headers={"Host": "222.143.24.250:98",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Referer": "http://222.143.24.250:98/",
                "Accept-Encoding": "gzip, deflate, sdch",
                "Accept-Language": "zh-CN,zh;q=0.8"}, timeout=600)
            return enp_html.text if enp_html.ok else None
        except:
            return None

    def pick_all(self):
        self.log.logger.info('开始获取河南企业信息')
        year = datetime.now().strftime('%Y')
        enp_datas = self.pick_enter_infos(year)
        enp_data_lists = json.loads(enp_datas)

        for enp in enp_data_lists:
            res = dict({k: None for k in self.qy_style})
            res['qy_name'] = enp['EnpName']
            res['qy_id'] = enp['EnpCode']
            res['province_id'] = self.province_id
            res['qy_jd'] = enp['Longitude']
            res['qy_wd'] = enp['Latitude']
            res['qy_corporation'] = enp['CorporationName']
            res['qy_organization_code'] = enp['CorporationCode']
            res['qy_url'] = self.href + "/EnpInfo.aspx?EnpCode=" + enp['EnpCode'] +"&InfoYear="

            qy_txt = self.pick_enter_info(res['qy_url'] + year)

            if qy_txt is None:
                continue

            tables = pq(qy_txt).find('table#tbenpinfo')
            trs = pq(tables).find('tr')

            res['qy_register_type'] = trs.eq(1).find('td').eq(1).text()
            res['qy_industry'] = trs.eq(1).find('td').eq(3).text()
            res['qy_wrylx'] = trs.eq(2).find('td').eq(1).text()
            res['qy_unit_category'] = trs.eq(3).find('td').eq(1).text() + "、" + trs.eq(2).find('td').eq(3).text()
            res['qy_scale'] = trs.eq(2).find('td').eq(5).text()
            res['qy_link_user'] = trs.eq(4).find('td').eq(1).text()
            res['qy_link_phone'] = trs.eq(4).find('td').eq(3).text()
            res['qy_fax'] = trs.eq(4).find('td').eq(5).text()
            res['qy_lead_time'] = trs.eq(5).find('td').eq(1).text()
            res['qy_address'] = trs.eq(6).find('td').eq(1).text()
            res['qy_auto_monitor_style'] = trs.eq(7).find('td').eq(1).text()
            res['qy_tysj'] = trs.eq(7).find('td').eq(3).text()
            res['qy_auto_monitor_operation_style'] = trs.eq(9).find('td').eq(1).text()
            self.log.logger.info(res)
            qy_message(res)

if __name__ == '__main__':
    t = time.time()
    ha = HAEmissionPicker()
    ha.pick_all()

    print('time----------------->', time.time() - t)
