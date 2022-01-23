# -*- coding: utf-8 -*-

from tgspiders.crawler.environmental_data.crawler_enterprise_environmental_data.base import Base
from tgspiders.lib.post_root import qy_decetion, get_qy_id_url_lasttime
from tgspiders.lib.float_util import float_cast
from datetime import datetime, timedelta
from pyquery import PyQuery as pq
from tgspiders.lib.log import Log
import time


class FJEmissionPickerData(Base):
    def __init__(self):
        super(FJEmissionPickerData, self).__init__('http://wryfb.fjemc.org.cn/')
        self.province_id = 35000000
        self.log = Log()
        self.href = 'http://wryfb.fjemc.org.cn/'

    def get_all_qyurl_by_provinceid(self, province_id, qy_style):
        list_qyinfo = []
        list_qy = get_qy_id_url_lasttime(province_id, qy_style)

        for k in list_qy:
            dev = dict()
            dev['qy_id'] = k['qyid']
            dev['qy_url'] = k['qyurl']
            dev['monitortime'] = k['monitortime'] if k['monitortime'] else '2019-01-01 00:00:00'
            list_qyinfo.append(dev)
        return list_qyinfo

    def pick_dev_data(self, qy_id, qy_url, serdate):
        try:
            res_html = self.http.session.post(qy_url, headers={
                "Host": "wryfb.fjemc.org.cn",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Accept-Encoding": "gzip, deflate",
                "Content-Type": "application/x-www-form-urlencoded",
                "Content-Length": "210",
                "Connection": "keep-alive",
                "Referer": "http://wryfb.fjemc.org.cn/page7.aspx?id=%s" % (qy_id,),
                "Upgrade-Insecure-Requests": "1"},
                                              data={
                                                  "__VIEWSTATE": "/wEPDwUJNDk2MTM2Mzc5ZGTd37nDAAZ8HMoQ9C6MjYnecXynQQ==",
                                                  "__EVENTVALIDATION": "/wEWAwKKm/SpBwKnpoOOCwKY7+/tCc29g5gXa+vZaoWCWvhGPER39rFI",
                                                  "right$l_date": serdate,
                                                  "right$Button1": "搜索"
                                              })
            return str(res_html.text) if res_html.ok else None
        except Exception as e:
            return None

    def pick_curr_dev_data(self, qy_url):
        try:
            res_html = self.http.session.get(qy_url,
                                             headers={"Host": "wryfb.fjemc.org.cn",
                                                      "Connection": "keep-alive",
                                                      "Upgrade-Insecure-Requests": "1",
                                                      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36",
                                                      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                                                      "Referer": "http://wryfb.fjemc.org.cn/page6.aspx?id=J519L5HF-03N5-NHDO-JELS-ZGX35LTQG80F&lawcode=75314528-X",
                                                      "Accept-Encoding": "gzip, deflate, sdch",
                                                      "Accept-Language": "zh-CN,zh;q=0.8"},
                                             timeout=600)
            return str(res_html.text) if res_html.ok else None
        except Exception as e:
            return None

    def insert_dev_datas(self, dev_datas, qy_id):
        dev_list = ['废气排放口', '汽电锅炉烟道', '脱硫塔']
        trs = pq(dev_datas).find('div.table3 table').find('tr')
        nowStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        nowDate = self.parser.set_date(nowStr).set_time(nowStr).datetime
        dev_name = ''
        timeStr = ''
        result = list()
        for i in range(1, trs.length):
            tds = trs.eq(i).find('td')
            pro_index = 0

            if (tds.length == 8):
                dev_name = tds.eq(0).text()
                timeStr = tds.eq(1).text() + ':00'
                pro_index = 2

            if dev_name in dev_list:
                dev_name = dev_name + '1'

            dev_name = dev_name.replace('１', '1').replace('２', '2')
            timeDate = self.parser.set_date(timeStr).set_time(timeStr).datetime

            if timeDate > nowDate:
                continue

            res = dict({k: None for k in self.sql_type})
            res['province_id'] = self.province_id
            res['enterprise_id'] = qy_id
            res['monitor_point'] = dev_name
            res['monitor_time'] = timeStr
            res['project_id'] = tds.eq(pro_index).text()
            res['monitor_value'] = float_cast(tds.eq(pro_index + 1).text()) if tds.eq(
                pro_index + 1).text() != '' else None
            res['standard_limit_value'] = float_cast(tds.eq(pro_index + 2).text()) if float_cast(
                tds.eq(pro_index + 2).text()) > 0 else None
            res['evaluation_criterion'] = '是否停产： ' + tds.eq(pro_index + 5).text()

            # self.log.logger.info(res)
            result.append(res)
        if result:
            qy_decetion(result)

    def pick_all(self):
        self.log.logger.info('开始获取福建环保数据')
        qy_infos = self.get_all_qyurl_by_provinceid(self.province_id, 1)
        for qy_info in qy_infos:
            qy_id = qy_info['qy_id']
            qy_url = qy_info['qy_url']

            last_update_time = datetime.strptime(qy_info['monitortime'], '%Y-%m-%d %H:%M:%S') + timedelta(hours=1)
            start_date = last_update_time.strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = self.parser.set_date(start_date).set_time('00:00:00').datetime
            end_date = self.parser.set_date(end_date).set_time('00:00:00').datetime
            days = (end_date - start_date).days + 1

            for i in range(0, days):
                serdate = (last_update_time + timedelta(days=i)).strftime('%Y-%m-%d')
                # serdate = '2019-09-02'
                dev_datas = self.pick_dev_data(qy_id, qy_url, serdate)
                if dev_datas is not None:
                    self.insert_dev_datas(dev_datas, qy_id)
            dev_datas = self.pick_curr_dev_data(qy_url.replace('page7.aspx?', 'page6.aspx?'))
            if dev_datas is not None:
                self.insert_dev_datas(dev_datas, qy_id)


if __name__ == '__main__':
    t = time.time()
    fj = FJEmissionPickerData()
    fj.pick_all()

    print('time---------------->', time.time() - t)
    # last_update_time = datetime.strptime("2019-01-14 15:00:00",'%Y-%m-%d %H:%M:%S')+timedelta(hours=1)
    # print(last_update_time)
