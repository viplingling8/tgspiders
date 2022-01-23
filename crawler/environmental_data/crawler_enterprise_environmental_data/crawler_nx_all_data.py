# -*- coding: utf-8 -*-

from tgspiders.crawler.environmental_data.crawler_enterprise_environmental_data.base import Base
from tgspiders.lib.post_root import qy_decetion, get_qy_id_url_lasttime
from tgspiders.lib.float_util import float_cast
from datetime import datetime, timedelta
from pyquery import PyQuery as pq
from tgspiders.lib.log import Log
import time


class NXEmissionPickerData(Base):
    def __init__(self):
        super(NXEmissionPickerData, self).__init__('http://119.60.12.114:3000/xxgk')
        self.province_id = 64000000
        self.log = Log()

    def get_all_qyurl_by_provinceid(self, province_id, qy_style):
        list_qyinfo = []
        list_qy = get_qy_id_url_lasttime(province_id, qy_style)

        for k in list_qy:
            if not k['monitortime']:
                k['monitortime'] = '2019-01-01 00:00:00'
            dev = dict()
            dev['qy_id'] = k['qyid']
            dev['qy_url'] = k['qyurl']
            dev['monitortime'] = k['monitortime']
            list_qyinfo.append(dev)
        return list_qyinfo

    def pick_dev_data(self, qy_url, host, cookie, dev_id, serdate):
        if host == '119.60.12.114:3000':
            res_html = self.http.session.get(qy_url,
                                             params={'devid': dev_id,
                                                     'serdate': serdate},
                                             headers={'Host': host,
                                                      'Connection': 'keep-alive',
                                                      'Upgrade-Insecure-Requests': '1',
                                                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
                                                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                                      'Accept-Encoding': 'gzip, deflate, sdch',
                                                      'Accept-Language': 'zh-CN,zh;q=0.8',
                                                      'Cookie': cookie},
                                             timeout=600)
        elif host == '119.60.9.17:9001' or host == '218.95.153.246:9002':
            res_html = self.http.session.get(qy_url,
                                             params={'serdate': serdate},
                                             headers={'Host': host,
                                                      'Connection': 'keep-alive',
                                                      'Upgrade-Insecure-Requests': '1',
                                                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
                                                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                                      'Accept-Encoding': 'gzip, deflate, sdch',
                                                      'Accept-Language': 'zh-CN,zh;q=0.8',
                                                      'Cookie': cookie},
                                             timeout=600)
        elif host == '119.60.0.59:20008':
            res_html = self.http.session.post(qy_url,
                                              params={'indexMenus': '',
                                                      'time': serdate},
                                              headers={'Host': host,
                                                       'Connection': 'keep-alive',
                                                       'Upgrade-Insecure-Requests': '1',
                                                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
                                                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                                       'Accept-Encoding': 'gzip, deflate, sdch',
                                                       'Accept-Language': 'zh-CN,zh;q=0.8',
                                                       'Cookie': cookie},
                                              timeout=600)
        else:
            return None

        return res_html.text if res_html.ok else None

    def insert_dev_datas(self, dev_datas, qy_id, host, serdate):
        if host == '119.60.12.114:3000' or host == '218.95.153.246:9002':
            project_list = [{'project_id': '烟尘', 'index': 2}, {'project_id': '二氧化硫', 'index': 7},
                            {'project_id': '氮氧化物', 'index': 12}]
            trs = pq(dev_datas).find('table #gasTbody').find('tr')
        elif host == '119.60.9.17:9001':
            project_list = [{'project_id': '烟尘', 'index': 3}, {'project_id': '二氧化硫', 'index': 9},
                            {'project_id': '氮氧化物', 'index': 15}]
            trs = pq(dev_datas).find('table #gasTbody').find('tr')
        elif host == '119.60.0.59:20008':
            project_list = [{'project_id': '烟尘', 'index': 2}, {'project_id': '二氧化硫', 'index': 6},
                            {'project_id': '氮氧化物', 'index': 10}]
            trs = pq(dev_datas).find('table #gasTbody').find('tr')

        for i in range(0, trs.length):
            tds = trs.eq(i).find('td')
            dev_name = tds.eq(0).text()
            timeStr = tds.eq(1).text() + ':00:00' if tds.eq(1).text() != '' else serdate + ' 00:00:00'
            timeDate = self.parser.set_date(timeStr).set_time(timeStr).datetime
            nowStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            nowDate = self.parser.set_date(nowStr).set_time(nowStr).datetime

            if timeDate > nowDate:
                continue

            for project in project_list:
                res = dict({k: None for k in self.sql_type})
                res['province_id'] = self.province_id
                res['enterprise_id'] = qy_id
                res['monitor_point'] = dev_name
                res['monitor_time'] = str(self.parser.set_date(timeStr).set_time(timeStr).datetime)
                res['project_id'] = project['project_id']
                res['monitor_value'] = float_cast(tds.eq(project['index']).text())
                res['standard_limit_value'] = float_cast(tds.eq(project['index'] + 1).text()) if float_cast(
                    tds.eq(project['index'] + 1).text()) > 0 else None
                res['evaluation_criterion'] = tds.eq(project['index'] + 2).text()
                self.log.logger.info(res)
                qy_decetion(res)

    def pick_all(self):
        self.log.logger.info('开始获取宁夏环保数据')
        qy_infos = self.get_all_qyurl_by_provinceid(self.province_id, 1)
        url = ''

        for qy_info in qy_infos:
            try:
                qy_id = qy_info['qy_id']
                qy_url = qy_info['qy_url']

                if qy_url is None:
                    continue

                if qy_url.find(url) == -1 or url == '':
                    url = qy_url.split('?')[0]
                    host = qy_url.split('/')[2]
                    purl = url.replace('info', 'list').replace('!qyxq.action', '.html')
                    res = self.http.session.get(purl + '/xxgk/qyhjxxgk.html')
                    cookie = 'JSESSIONID=' + res.cookies['JSESSIONID'] if res.ok else None

                dev_id = 3
                # last_update_time = self.get_last_update_time(self.province_id, qy_id)
                last_update_time = datetime.strptime(qy_info['monitortime'], '%Y-%m-%d %H:%M:%S')
                start_date = last_update_time.strftime('%Y-%m-%d')
                end_date = datetime.now().strftime('%Y-%m-%d')
                start_date = self.parser.set_date(start_date).set_time('00:00:00').datetime
                end_date = self.parser.set_date(end_date).set_time('00:00:00').datetime
                days = (end_date - start_date).days + 1

                for i in range(0, days):
                    serdate = (last_update_time + timedelta(days=i)).strftime('%Y-%m-%d')
                    dev_datas = self.pick_dev_data(qy_url, host, cookie, dev_id, serdate)

                    if dev_datas is not None:
                        self.insert_dev_datas(dev_datas, qy_id, host, serdate)

            except Exception as e:
                print(e)


if __name__ == '__main__':
    t = time.time()
    nx = NXEmissionPickerData()
    nx.pick_all()
    print('time----------------->', time.time() - t)
