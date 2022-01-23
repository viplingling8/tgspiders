# -*- coding: utf-8 -*-

from tgspiders.lib.post_root import qy_decetion
from tgspiders.lib.log import Log
from pyquery import PyQuery as pq
import requests
import datetime
import json


class XSSmissionPickerData:
    def __init__(self):
        self.province_id = 42000000
        self.enterprise_id = '3001'
        self.log = Log()
        self.base_url = 'http://113.57.151.5:4504/AutoData/Business/HisData/HisData_List.aspx?HourStopBS=Show'
        self.cookie_dict = {
            '1#机组烟气排放口': '17325360909654',
            '2#机组烟气排放口': '17325360811525',
            '3#机组烟气排放口': 'HD071413107703',
            '4#机组烟气排放口': 'SDL07142014802'
        }

    def get_data(self):
        end_time = datetime.datetime.now()
        offset = datetime.timedelta(days=-3)
        start_time = (end_time + offset).strftime('%Y-%m-%d %H:%M:%S')

        for jizu_name, jizu_code in self.cookie_dict.items():
            headers = {
                'Cookie': 'LHP3_SysCode=SysCode=EAFMS; ASP.NET_SessionId=uj5di5tb0hury453hpcjqrgb;'
                          ' USER_COOKIE=UserName=Wv1kEE4I+ucNvpfjTsSteg==&UserPassword=;'
                          ' LHP3_Web=UserID=mjPnuhJf4N8=&UserName=Wv1kEE4I+ucNvpfjTsSteg==&RealName'
                          '=Wv1kEE4I+ucNvpfjTsSteg==&RoleID=kpDE1i7N/wQ=&RoleName=YoT+yddBXSsbtbte3Zmq2A'
                          '==&UnitID=QbbXd+MsW9bBq4F3FBrzs8nFKQ0JbXtxkUcph7FnhBpv422ufR+M6Q==&FullPath='
                          '&BelongSystem=sCPp083xSTc=; PChange=1; SelectItem=stime=2019-11-28+00%3a00%3a00'
                          '&etime=2019-11-29+20%3a10%3a00; CurrPageUrl=%2FAutoData%2FBusiness%2FHisData%2'
                          'FHisData_List.aspx%3FHourStopBS%3DShow; checkedNode=' + jizu_code + '; checked'
                                                                                               'NodeName=%E6%B9%96%E5%8C%97%E5%8D%8E%E7%94%B5%E8%A5%BF%E5%A1%9E%E5%B1%B1'
                                                                                               '%E5%8F%91%E7%94%B5%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B84%E5%8F%B7%E6%9C%BA%E7%BB'
                                                                                               '%84%E7%83%9F%E6%B0%94%E6%8E%92%E6%94%BE%E5%8F%A3',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Chrome/75.0.3770.100 Safari/537.36'
            }

            data = {
                'action': 'query',
                'stime': start_time,
                'etime': str(end_time)[:19],
                'parament': 'ZA9,ZB0,ZB1,ZB2,ZB3,ZB4,ZB5,ZB7,ZD1,K20,Z92',
                'paramentname': '烟尘,烟气流速,烟气压力,SO2,NOx,O2含量,CO,烟气湿度,烟气温度,锅炉负荷,废气流量',
                'seldatatype': '2061',
                'valuetype': 'Avg,ZsAvg,Cou',
                'curpage': '1',
                'currowNum': '100',
                'dataflag': '',
                'isstop': 'false'
            }

            r2 = requests.post(url=self.base_url, headers=headers, data=data)
            print(r2.ok, r2.text)
            index_jsons = json.loads(r2.text)
            index_json = index_jsons[3]
            item = index_json.get('DataView')
            rows = item.get('rows')

            for li in rows:
                yanchen = pq(li.get('ZA9(折算均值)')).text()
                NOx = pq(li.get('ZB3(折算均值)')).text()
                SO2 = pq(li.get('ZB2(折算均值)')).text()
                time_stamp = li.get('DataTime')
                yield {
                    '机组': jizu_name,
                    'date': time_stamp,
                    '二氧化硫': SO2,
                    '氮氧化物': NOx,
                    '烟尘': yanchen
                }

    def pick_all(self):
        result = list()
        for data in self.get_data():
            res = dict()
            res['enterprise_id'] = self.enterprise_id
            res['province_id'] = self.province_id
            res['monitor_point'] = data['机组']
            res['monitor_time'] = data['date'] + ':00'
            res['evaluation_criterion'] = ''
            lis = {'二氧化硫': 50, '氮氧化物': 100, '烟尘':  20}

            for li, val in lis.items():
                res['monitor_value'] = data.get(li)
                res['standard_limit_value'] = val
                res['project_id'] = li
                self.log.logger.info(res)
                result.append(res)
        if result:
            qy_decetion(result)


if __name__ == '__main__':
    xxs = XSSmissionPickerData()
    xxs.pick_all()
