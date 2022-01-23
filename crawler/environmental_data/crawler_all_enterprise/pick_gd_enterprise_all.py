# -*- coding: utf-8 -*-

from tgspiders.crawler.environmental_data.crawler_all_enterprise.base import Base
from tgspiders.lib.post_root import qy_message
from pyquery import PyQuery as pq
from tgspiders.lib.log import Log
import requests
import time

requests.packages.urllib3.disable_warnings()

class GDEmissionPicker(Base):
    def __init__(self):
        super(GDEmissionPicker, self).__init__('https://app.gdep.gov.cn/epinfo/')
        self.log = Log()
        self.province_id = 44000000

    def get_province(self, res_html):
        lit = []
        lis = pq(res_html)('#nav li:gt(1) a')

        for li in lis.items():
            lit.append(li.attr('onclick').split("'")[1])
        return lit

    def pick_qy(self, data):
        trs = pq(data)('#EnterpriseVo tr')

        for tr in trs.items():
            city = tr.find('td').eq(1).text()
            num = tr.find('td').find('a').eq(0).attr('onclick').split('"')[1]
            name = tr.find('td').find('a').eq(0).attr('onclick').split('"')[3]
            url = 'https://app.gdep.gov.cn/epinfo/selfmonitor/getEnterpriseInfo/%s?ename=%s'%(num, name)
            r = self.http.session.get(url=url, verify=False)

            if r.ok:
                tr_s = pq(r.text)('.widget-content table tr')
                # print(tr_s.eq(1).find('td').text())
                res = dict({k: None for k in self.qy_style})
                res['qy_name'] = name
                res['qy_id'] = num
                res['province_id'] = self.province_id
                res['qy_industry'] = tr_s.eq(3).find('td').text()
                res['qy_address'] = tr_s.eq(4).find('td').text()
                res['qy_organization_code'] = tr_s.eq(1).find('td').text()
                res['qy_url'] = url
                res['qy_city'] = city
                self.log.logger.info(res)
                qy_message(res)

    def pick_all(self):
        self.log.logger.info('开始获取广东企业信息')
        res_html = self.http.session.get('https://app.gdep.gov.cn/epinfo/',verify=False)
        cookie = 'JSESSIONID=' + res_html.cookies['JSESSIONID'] if res_html.ok else None

        if cookie is None:
            return
        lit = self.get_province(res_html.text)

        for id in lit:
            url = 'https://app.gdep.gov.cn/epinfo/region/%s/1?ename=&year=2019'%(id,)
            r = self.http.session.get(url=url, verify=False)
            self.pick_qy(r.text)

if __name__ == '__main__':
    t = time.time()
    gd = GDEmissionPicker()
    gd.pick_all()

    print('time----------------->', time.time() - t)