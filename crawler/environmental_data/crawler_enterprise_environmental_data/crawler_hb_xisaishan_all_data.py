# -*- coding: utf-8 -*-

from tgspiders.crawler.environmental_data.crawler_enterprise_environmental_data.base import Base
from tgspiders.lib.post_root import qy_decetion, get_qy_id_url_lasttime
from tgspiders.lib.log import Log
from pyquery import PyQuery as pq
import requests
import json
import re
import datetime


class XSSmissionPickerData(Base):
    """docstring for CrawlerHbXYAllData"""

    def __init__(self):
        super(XSSmissionPickerData, self).__init__('http://113.57.151.5:4504/')
        # self.auth = HTTPBasicAuth('肖南海'.encode('utf-8'), 'xss@5508')
        self.province_id = 42000000
        self.log = Log()
        self.session = requests.Session()
        self.headers = {
            'Host': '113.57.151.5:4504',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }

    def login(self):
        r = self.session.get('http://113.57.151.5:4504/', headers=self.headers)
        if r.ok:
            __VIEWSTATE = pq(r.text)("#__VIEWSTATE").val()
            __VIEWSTATEGENERATOR = pq(r.text)("#__VIEWSTATEGENERATOR").attr('value')
            __EVENTVALIDATION = pq(r.text)("#__EVENTVALIDATION").val()
            data = {'__VIEWSTATE': __VIEWSTATE, '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
                    '__EVENTVALIDATION': __EVENTVALIDATION, 'txtUserNme': '肖南海', 'txtPassWord': 'xss@5508',
                    'chkRememberMe': 'on', 'butOK': ''}
            rs = self.session.post('http://113.57.151.5:4504/', headers=self.headers, data=data)
            return rs.ok

    def crawl(self, start_date, end_date):
        rs = self.session.post('http://113.57.151.5:4504/EAFMS/AjaxHandler/MNTreeData.ashx?cType=0',
                               headers=self.headers)
        if rs.ok:
            dt = rs.json()[0]
            childrens = dt.get('children')[0].get('children')[0].get('children')[0].get('children')
            unit_info = {item['id']: item['text'] for item in childrens}
            result = list()
            for key, jizu in unit_info.items():
                if jizu == '1号机组烟气排放口':
                    id_ = 1
                elif jizu == '2号机组烟气排放口':
                    id_ = 2
                elif jizu == '3号机组烟气排放口':
                    id_ = 3
                elif jizu == '4号机组烟气排放口':
                    id_ = 4
                else:
                    id_ = 6
                coo = "LHP3_SysCode={}; ASP.NET_SessionId={}; USER_COOKIE={}; LHP3_Web={}; " \
                      "CurrPageUrl=%2FAutoData%2FBusiness%2FHisData%2FHisData_List.aspx%3FHourStopBS%3DShow; " \
                      "PChange=1; checkedNode={}; " \
                      "checkedNodeName={}%E5%8F%B7%E6%9C%BA%E7%BB%84%E7%83%9F%E6%B0%94%E6%8E%92%E6%94%BE%E5%8F%A3; " \
                      "SelectItem=stime={}&etime={}".format(
                    self.session.cookies['LHP3_SysCode'], self.session.cookies['ASP.NET_SessionId'],
                    self.session.cookies['USER_COOKIE'], self.session.cookies['LHP3_Web'], key, id_, start_date,
                    end_date)
                header = {
                    "Host": "113.57.151.5:4504",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
                    "Accept": "*/*",
                    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                    "Accept-Encoding": "gzip, deflate",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "X-Requested-With": "XMLHttpRequest",
                    "Content-Length": "556",
                    "Origin": "http://113.57.151.5:4504",
                    "Connection": "keep-alive",
                    "Referer": "http://113.57.151.5:4504/AutoData/Business/HisData/HisData_List.aspx?HourStopBS=Show",
                    'Cookie': coo,
                    "Pragma": "no-cache",
                    "Cache-Control": "no-cache",
                }
                r = self.session.post(
                    'http://113.57.151.5:4504/AutoData/Business/HisData/HisData_List.aspx?HourStopBS=Show',
                    headers=header, data={
                        "action": "query",
                        "stime": start_date,
                        "etime": end_date,
                        "parament": "ZA9,ZB0,ZB1,ZB2,ZB3,ZB4,ZB5,ZB7,ZD1,K20,Z92",
                        "paramentname": "烟尘,烟气流速,烟气压力,SO2,NOx,O2含量,CO,烟气湿度,烟气温度,锅炉负荷,废气流量",
                        "seldatatype": "2061",
                        "valuetype": "Avg,ZsAvg,Cou",
                        "curpage": "1",
                        "currowNum": "42",
                        "dataflag": "",
                        "isstop": "false",
                        "IsRevise": "true"
                    })
                if r.ok:
                    con = json.loads(r.text)
                    values = con[3]["DataView"]['rows']
                    for dic in values:
                        for id_ in ["氮氧化物", "烟尘", '二氧化硫']:
                            if id_ == '氮氧化物':
                                vas = 'ZB3(折算均值)'
                                standard_limit_value = 50
                            elif id_ == '烟尘':
                                vas = 'ZA9(折算均值)'
                                standard_limit_value = 10
                            else:
                                vas = 'ZB2(折算均值)'
                                standard_limit_value = 35
                            res = dict({k: None for k in self.sql_type})
                            res['province_id'] = self.province_id
                            res['enterprise_id'] = 3001
                            res['monitor_point'] = jizu
                            res['monitor_time'] = dic['DataTime']
                            res['project_id'] = id_
                            res['monitor_value'] = re.findall('>(.*?)<', dic[vas])[0]
                            res['standard_limit_value'] = standard_limit_value
                            res['evaluation_criterion'] = 'null'
                            self.log.logger.info(res)
                            result.append(res)
            if result:
                qy_decetion(result)

    def pick_all(self):
        # last_update_time = get_qy_id_url_lasttime(self.province_id, 1)
        # start_date = last_update_time[2]['monitortime']
        start_date = (datetime.datetime.now() - datetime.timedelta(days=20)).strftime('%Y-%m-%d %H:%M:%S')
        end_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if self.login():
            # self.crawl('2020-08-15 00:00:00', '2020-08-17 11:47:00')
            self.crawl(start_date, end_date)


if __name__ == '__main__':
    xy = XSSmissionPickerData()
    xy.pick_all()
