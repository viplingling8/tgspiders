# -*- coding: utf-8 -*-

from tgspiders.crawler.environmental_data.crawler_all_enterprise.base import Base
from tgspiders.lib.post_root import qy_message
from tgspiders.lib.err_util import retry
from tgspiders.lib.log import Log
from datetime import datetime
import time
import json


class SDEmissionPicker(Base):
    def __init__(self):
        super(SDEmissionPicker, self).__init__('http://58.56.98.78:8405')
        self.province_id = 37000000
        self.log = Log()
        self.href = 'http://58.56.98.78:8405'
        self.city_href = {
                            # '济南': 'http://119.164.252.34:8403',  # 无效
                            '济南': 'http://221.214.107.80:8403/',
                            '青岛': 'http://219.147.6.195:8403',
                            '淄博': 'http://60.210.111.130:8406',
                            # '枣庄': 'http://218.56.152.39:8403',   # 无效
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

    @retry
    def pick_enter_infos(self, cookie, year):
        try:
            res_html = self.http.session.post('http://58.56.98.78:8405/ajax/npublic/Index.ashx?jsoncallback=jQuery111103948804758501945_1482218806776',
                                              headers={'Connection': 'keep-alive',
                                                        'Content-Length': '104',
                                                        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
                                                        'Origin': 'http://58.56.98.78:8405',
                                                        'X-Requested-With': 'XMLHttpRequest',
                                                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36',
                                                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                                        'Referer': 'http://58.56.98.78:8405/',
                                                        'Accept-Encoding': 'gzip, deflate',
                                                        'Accept-Language': 'zh-CN,zh;q=0.8',
                                                        'Cookie':  cookie},
                                             data={'IsBeginZxjc': '2',
                                                    'Method': 'LoadGrid',
                                                    'SubType': '2',
                                                    'Year': year,
                                                    'areaCode': '0',
                                                    'cityCode': '0',
                                                    'EntName': '',
                                                    'page': '1',
                                                    'rows': '500'},
                                              timeout=600)
            const = res_html.text if res_html.ok else None

            if const is None:
                return None

            const = const.replace('jQuery111103948804758501945_1482218806776(', '').replace(')', '')
            enterInfos = json.loads(const)
            return enterInfos['rows']
        except:
            return None

    @retry
    def pick_enter_info(self, ent_href, cityName, entCode, year):
        try:
            jsoncallback = 'jQuery11110043904820099857744_1482223108531'
            # print(self.city_href[cityName] + '/ajax/npublic/NEnterprise.ashx')
            ent_html = self.http.session.get(self.city_href[cityName] + '/ajax/npublic/NEnterprise.ashx',
                                  headers={'Connection': 'keep-alive',
                                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36',
                                        'Accept': '*/*',
                                        'Referer': ent_href,
                                        'Accept-Encoding': 'gzip, deflate, sdch',
                                        'Accept-Language': 'zh-CN,zh;q=0.8'},
                                  params={'Method': 'GetData',
                                        'jsoncallback': jsoncallback,
                                        'EntCode': entCode,
                                        'Year': year,
                                        '_': '1482223108532'},
                                  timeout=600)

            const = ent_html.text if ent_html.ok else None

            if const is None:
                return None

            const = const.replace(jsoncallback, '').replace('(', '').replace(')', '')
            enterInfo = json.loads(const)
            return enterInfo
        except Exception as e:
            return None

    @retry
    def get_cookie(self):
        try:
            res_html = self.http.session.post('http://58.56.98.78:8405/ajax/CompatibleHandler.ashx',
                                          headers={'Connection': 'keep-alive',
                                                    'Content-Length': '78',
                                                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                                                    'Origin': 'http://58.56.98.78:8405',
                                                    'X-Requested-With': 'XMLHttpRequest',
                                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36',
                                                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                                    'Referer': 'http://58.56.98.78:8405/',
                                                    'Accept-Encoding': 'gzip, deflate',
                                                    'Accept-Language': 'zh-CN,zh;q=0.8'},
                                         data={'Method': 'LoadAreas',
                                                'Rand': '0.20796503918153286',
                                                'NeedAll': 'true',
                                                'CityCode': '0'},
                                          timeout=600)
            cookie = 'ASP.NET_SessionId=' + res_html.cookies['ASP.NET_SessionId'] if res_html.ok else None
            return cookie
        except:
            return None

    def pick_all(self):
        self.log.logger.info('开始获取山东企业信息')
        cookie = self.get_cookie()

        if cookie is None:
            return

        year = datetime.now().strftime('%Y')
        enp_list = self.pick_enter_infos(cookie, year)

        if enp_list is None:
            return

        for ent in enp_list:
            entCode = ent['EntCode']
            cityCode = ent['CityCode']
            cityName = ent['CityName']
            ent_href = self.href + '/Ent/' + cityCode + '/' + year + '/' + entCode
            con_txt = self.pick_enter_info(ent_href, cityName, entCode, year)

            if con_txt is None:
                continue

            res = dict({k: None for k in self.qy_style})
            res['qy_name'] = ent['EntName']
            res['qy_id'] = entCode
            res['province_id'] = self.province_id
            res['qy_city'] = cityName
            res['qy_city_id'] = cityCode
            res['qy_url'] = ent_href
            res['qy_wrylx'] = ent['EntTypeName']

            if len(con_txt) != 0:
                res['qy_introduce'] = con_txt['Remark']
                res['qy_organization_code'] = con_txt['AgencyCode']
                res['qy_address'] = con_txt['Address']
                res['qy_jd'] = con_txt['Longitude']
                res['qy_wd'] = con_txt['Latitude']
                res['qy_corporation'] = con_txt['Legal']
                res['qy_industry'] = con_txt['IndType']
                res['qy_link_user'] = con_txt['Contacts']
                res['qy_link_phone'] = con_txt['Phone']
                res['qy_manager_dept'] = con_txt['EntrustCompany']
                res['qy_lead_time'] = con_txt['Produce']

            self.log.logger.info(res)
            qy_message(res)

if __name__ == '__main__':
    t = time.time()
    sd = SDEmissionPicker()
    sd.pick_all()
    print('time----------------->', time.time() - t)
