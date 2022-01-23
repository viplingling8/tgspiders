# -*- coding: utf-8 -*-

import time
import requests
from pyquery import PyQuery as pq
from datetime import datetime
from tgspiders.crawler.environmental_data.crawler_all_enterprise.base import Base

from tgspiders.lib.log import Log


class LNEmissionPicker(Base):
    def __init__(self):
        super(LNEmissionPicker, self).__init__('http://218.60.144.99:8087/')
        self.province_id = 21000000
        self.log = Log().logger
        self.href = 'http://218.60.144.99:8087'
        self.session = requests.Session()

    def pick_citys(self, year):
        try:
            self.log.info('获取辽宁所有地区以及地区ID')
            res_html = self.session.get(
                self.href + '/?year=' + year, timeout=600)
            const = res_html.text if res_html.ok else None

            if const is None:
                return None

            trs = pq(const).find('div#div1 table').find('tr')
            cityInfos = []

            for i in range(1, trs.length - 1):
                a = pq(trs.eq(i).find('td').eq(0).find('a').eq(0))
                cityInfo = {}
                cityInfo["href"] = a.attr('href')
                cityInfo["id"] = cityInfo["href"].replace('/Main/City/', '')
                cityInfo["name"] = a.text()
                cityInfos.append(cityInfo)

            return cityInfos
        except Exception as e:
            self.log.error('获取辽宁所有地区以及地区ID失败,%s' % e.message)

    def pick_enter_infos(self, city_href):
        try:
            res_html = self.session.get(
                self.href + city_href, timeout=600)
            const = res_html.text if res_html.ok else None

            if const is None:
                return None

            lis = pq(const).find('div.dragbox-content').find('li')
            enpInfos = []

            for item in lis:
                a = pq(item).find('a')
                enpInfo = {}
                enpInfo["href"] = a.attr('href')
                enpInfo["id"] = enpInfo["href"].replace(
                    '/Main/Enterprise/', '')
                enpInfo["name"] = a.attr('title')
                enpInfo["info"] = pq(const).find(
                    'div#enterprise-info-' + enpInfo["id"]).find('table')
                enpInfos.append(enpInfo)

            return enpInfos
        except Exception as e:
            self.log.error('获取辽宁地区链接:%s失败,%s' % (city_href, e.message))

    def pick_all(self):
        year = datetime.now().strftime('%Y')
        city_list = self.pick_citys(year)

        for city_info in city_list:
            enp_list = self.pick_enter_infos(city_info['href'])
            city_id = city_info['id']
            city_name = city_info['name']
            self.log.info('开始获取 %s 数据, 共有%s个企业' % (city_name, len(enp_list)))

            for enp in enp_list:
                con_txt = enp['info']
                trs = pq(con_txt).find('tr')
                qy_wrylx = trs.eq(0).find('td').eq(0).find('span').eq(1).text()

                # if qy_wrylx != '' and '废气' not in qy_wrylx:
                #     continue

                res = dict({k: None for k in self.qy_style})
                res['qy_name'] = enp['name']
                res['qy_id'] = enp['id']
                res['province_id'] = self.province_id
                res['qy_city'] = city_name
                res['qy_city_id'] = city_id
                res['qy_url'] = self.href + enp['href']
                res['qy_wrylx'] = qy_wrylx
                spans = trs.eq(1).find('td').eq(1).find('span')
                res['qy_industry'] = spans.eq(spans.length - 1).text()
                spans = trs.eq(2).find('td').eq(1).find('span')
                res['qy_corporation'] = spans.eq(spans.length - 1).text()
                spans = trs.eq(3).find('td').eq(0).find('span')
                res['qy_lead_time'] = spans.eq(spans.length - 1).text()
                spans = trs.eq(4).find('td').eq(0).find('span')
                res['qy_address'] = spans.eq(spans.length - 1).text()
                spans = trs.eq(5).find('td').eq(0).find('span')
                res['qy_link_user'] = spans.eq(spans.length - 1).text()
                spans = trs.eq(5).find('td').eq(1).find('span')
                res['qy_link_phone'] = spans.eq(spans.length - 1).text()
                spans = trs.eq(6).find('td').eq(0).find('span')
                res['qy_fax'] = spans.eq(spans.length - 1).text()
                spans = trs.eq(7).find('td').eq(0).find('span')
                res['qy_link_email'] = spans.eq(spans.length - 1).text()
                spans = trs.eq(8).find('td').eq(1).find('span')
                res['qy_manager_dept'] = spans.eq(spans.length - 1).text()

                self.insert_enterprise_info(res)


if __name__ == '__main__':
    t = time.time()
    ln = LNEmissionPicker()
    ln.pick_all()
    print('time----------------->', time.time() - t)
