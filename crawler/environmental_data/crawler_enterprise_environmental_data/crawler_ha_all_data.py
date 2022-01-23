# -*- coding: utf-8 -*-

from tgspiders.crawler.environmental_data.crawler_enterprise_environmental_data.base import Base
from tgspiders.lib.post_root import qy_decetion, get_qy_id_url_lasttime
from tgspiders.lib.float_util import float_cast
from datetime import datetime, timedelta
from pyquery import PyQuery as pq
from tgspiders.lib.log import Log
import time


class HAEmissionPickerData(Base):
    def __init__(self):
        super(HAEmissionPickerData, self).__init__('http://222.143.24.250:98/')
        self.log = Log()
        self.province_id = 41000000

    def get_all_qyurl_by_provinceid(self, province_id, qy_style):
        list_qyinfo = []
        list_qy = get_qy_id_url_lasttime(province_id, qy_style)
        for k in list_qy:
            dev = dict()
            if not k['monitortime']:
                k['monitortime'] = '2019-01-01 00:00:00'
            dev['qy_id'] = k['qyid']
            dev['qy_url'] = k['qyurl']
            dev['monitortime'] = k['monitortime']
            list_qyinfo.append(dev)
        return list_qyinfo

    def pick_dev_data(self, qy_url, serdate, year, todayDate, lastDate, page):
        qy_wrylx = "2"
        try:
            res_html = self.http.session.post(qy_url,
                                              headers={"Host": "222.143.24.250:98",
                                                       "Connection": "keep-alive",
                                                       "Content-Length": "5410",
                                                       "Cache-Control": "no-cache",
                                                       "Origin": "http://222.143.24.250:98",
                                                       "X-Requested-With": "XMLHttpRequest",
                                                       "X-MicrosoftAjax": "Delta=true",
                                                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36",
                                                       "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                                       "Accept": "*/*",
                                                       "Referer": qy_url,
                                                       "Accept-Encoding": "gzip, deflate",
                                                       "Accept-Language": "zh-CN,zh;q=0.8"},
                                              data={"ScriptManager1": "UpdatePanel2|Asp_AutoData",
                                                    "rd_DataType": qy_wrylx,
                                                    "txtStartDate_autoData": serdate,
                                                    "txtEndDate_autoData": serdate,
                                                    "Asp_AutoData_input": page,
                                                    "rd_SiteType": "2",
                                                    "txtStartDate_handData": lastDate,
                                                    "txtEndDate_handData": todayDate,
                                                    "txtStartDate_NoiseData": year,
                                                    "Asp_NoiseData_input": "1",
                                                    "txtStartDate_otherData": lastDate,
                                                    "txtEndDate_otherData": todayDate,
                                                    "txt_reason": year,
                                                    "ASP_Reason_input": "1",
                                                    "txt_monplan": year,
                                                    "Asp_MonPlan_input": "1",
                                                    "txtyearreport": year,
                                                    "__VIEWSTATE": "/wEPDwULLTE1NDA0NTMxOTUPFgQeBGZsYWcFATEeCGVucG1vZGVsMocRAAEAAAD/////AQAAAAAAAAAMAgAAAE1QU01vbml0b3JEYXRhUHViLk1vZGVsLCBWZXJzaW9uPTEuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49bnVsbAUBAAAAJVBTTW9uaXRvckRhdGFQdWIuTW9kZWwuRW50ZXJwcmlzZUluZm9CAAAACV9pbmZveWVhcghfZW5wY29kZQdfcHNjb2RlCF9lbnBuYW1lC19yZWdpb25jb2RlC19yZWdpb25uYW1lD19yZWdpc3R0eXBlY29kZQ9fcmVnaXN0dHlwZW5hbWUNX3VuaXR0eXBlY29kZQ1fdW5pdHR5cGVuYW1lEV9pbmR1c3RyeXR5cGVjb2RlEV9pbmR1c3RyeXR5cGVuYW1lDV91bml0c2l6ZWNvZGUNX3VuaXRzaXplbmFtZQxfcHNjbGFzc2NvZGUMX3BzY2xhc3NuYW1lC192YWxsZXljb2RlC192YWxsZXluYW1lC19lbnBhZGRyZXNzCl9sb25naXR1ZGUJX2xhdGl0dWRlDV9wcm9kdWN0cGhhc2UTX2VucGVudmlyb25tZW50ZGVwdBVfZW52aXJvbm1lbnRwcmluY2lwYWwQX2Vudmlyb25tZW50bWFucxBfY29ycG9yYXRpb25jb2RlEF9jb3Jwb3JhdGlvbm5hbWUMX29mZmljZXBob25lBF9mYXgMX21vYmlsZXBob25lBl9lbWFpbAtfcG9zdGFsY29kZRBfY29tbXVuaWNhdGVhZGRyCF9saW5rbWFuCF9vcmFpbmZvFF9hdHRlbnRpb25kZWdyZWVjb2RlFF9hdHRlbnRpb25kZWdyZWVuYW1lDF9wc2NsYXNzdHlwZRBfcHNjbGFzc3R5cGVuYW1lCV9lbnBzdGF0ZQxfZW5wc3RhdGVzdHIHX3JlbWFyawlfcHVic3RhdGULX3VwZGF0ZWRhdGUIX2lzMzBXS1cNX2lzaGVhdnltZXRhbBJfYXV0b0RhdGFJc0F1dG9QdWIOX2lzU2Vhc29uYWxQcm8IX2lzQnJlZWQJX3Byb3ZpbmNlBV9jaXR5B19jb3VudHkJX3Rvd25zaGlwCV9kaXN0cmljdAVfaWZzbQdfc21kYXRlDF9u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",
                                                    "__VIEWSTATEGENERATOR": "239CFCF6",
                                                    "__EVENTTARGET": "Asp_AutoData",
                                                    "__EVENTARGUMENT": "",
                                                    "__EVENTVALIDATION": "/wEWFwL8q4jOAQKorpHnDAKmwbsJArSmvrkOAo6Z2ssIAq2z2eEHAs3aq+0JAszaq+0JAsK1gYMFAvSzpO8PAuOdyYcHAvqy3LoKAsjZx+kGAtWdxG0CzsjNsgYCzYq62wEC47Pt6gkCjsD7oAUCxtOG6ggCpYWPnwoCufr59wQC3riumwQCy/yW6Qk2zHYm4pLfKxzO2XbbGoifUW33UW3bO7CI0h+3kmM29g==",
                                                    "__ASYNCPOST": "true"},
                                              timeout=600)
            return res_html.text if res_html.ok else None
        except:
            return None

    def insert_dev_datas(self, dev_datas, qy_id):
        dev_list = ['#1脱硫原烟气', '#2脱硫原烟气']
        trs = pq(dev_datas).find('table#tbdata_auto').find('tr')
        nowStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        nowDate = self.parser.set_date(nowStr).set_time(nowStr).datetime

        if trs.length < 3:
            return

        for i in range(2, trs.length):
            tds = trs.eq(i).find('td')

            if tds.length == 0:
                continue

            if tds.length > 13:
                pro_index_begin = 1
            else:
                pro_index_begin = 0

            dev_name = tds.eq(3).text()
            running_str = tds.eq(12 + pro_index_begin).text()

            if dev_name in dev_list:
                continue

            if '3#和4#排气筒采样孔' == dev_name:
                dev_name = '1#脱硫塔'
            elif '5#和6#排气筒采样孔' == dev_name:
                dev_name = '2#脱硫塔'
            elif '420t/h锅炉1' == dev_name:
                dev_name = '锅炉1'
            elif '420t/h锅炉2' == dev_name:
                dev_name = '锅炉2'
            elif '1081.2t/h锅炉1' == dev_name:
                dev_name = '锅炉1'
            elif '1081.2t/h锅炉2' == dev_name:
                dev_name = '锅炉2'
            elif '1900t/h锅炉1' == dev_name:
                dev_name = '锅炉1'
            elif '1900t/h锅炉2' == dev_name:
                dev_name = '锅炉2'
            elif '１#机组烟囱入口' == dev_name:
                dev_name = '1#机组烟囱入口'

            timeStr = tds.eq(1).text() + ':00:00'
            timeDate = self.parser.set_date(timeStr).set_time(timeStr).datetime

            if timeDate > nowDate:
                continue

            res = dict({k: None for k in self.sql_type})
            res['province_id'] = self.province_id
            res['enterprise_id'] = qy_id
            res['monitor_point'] = dev_name
            res['monitor_time'] = timeStr
            res['project_id'] = tds.eq(2).text()
            res['monitor_value'] = float_cast(tds.eq(4).text()) if tds.eq(4).text() != '' else None
            res['standard_limit_value'] = float_cast(
                tds.eq(6 + pro_index_begin).text().replace('<', '').replace('=', '')) if float_cast(
                tds.eq(6 + pro_index_begin).text().replace('<', '').replace('=', '')) > 0 else None

            if running_str is not None and running_str != '':
                res['evaluation_criterion'] = running_str
            self.log.logger.info(res)
            qy_decetion(res)

    def pick_all(self):
        self.log.logger.info('开始获取河南环保数据！')
        qy_infos = self.get_all_qyurl_by_provinceid(self.province_id, 1)
        nowDate = datetime.now()
        year = nowDate.strftime('%Y')
        todayDate = nowDate.strftime('%Y-%m-%d')
        lastDate = (nowDate + timedelta(days=-7)).strftime('%Y-%m-%d')
        for qy_info in qy_infos:
            qy_id = qy_info['qy_id']
            qy_url = qy_info['qy_url'] + year
            # last_update_time = self.get_last_update_time(self.province_id, qy_id)
            last_update_time = datetime.strptime(qy_info['monitortime'], '%Y-%m-%d %H:%M:%S')
            start_date = last_update_time.strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = self.parser.set_date(start_date).set_time('00:00:00').datetime
            end_date = self.parser.set_date(end_date).set_time('00:00:00').datetime
            days = (end_date - start_date).days + 1

            for i in range(0, days):
                serdate = (last_update_time + timedelta(days=i)).strftime('%Y-%m-%d')
                dev_datas = self.pick_dev_data(qy_url, serdate, year, todayDate, lastDate, "1")
                if dev_datas is None:
                    continue

                self.insert_dev_datas(dev_datas, qy_id)
                pages_info = pq(dev_datas).find('#Asp_AutoData table').find('tr').find('td')

                if str(pages_info) == '':
                    continue

                pages = pages_info.eq(1).text().split('，共')[1].replace('页', '')

                if pages == '' or int(pages) < 2:
                    continue

                for page in range(2, int(pages) + 1):
                    dev_datas = self.pick_dev_data(qy_url, serdate, year, todayDate, lastDate, str(page))

                    if dev_datas is not None:
                        self.insert_dev_datas(dev_datas, qy_id)


if __name__ == '__main__':
    t = time.time()
    ha = HAEmissionPickerData()
    ha.pick_all()
    print('time---------------->', time.time() - t)
