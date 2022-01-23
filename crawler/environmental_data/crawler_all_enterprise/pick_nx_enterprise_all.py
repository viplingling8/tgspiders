# -*- coding: utf-8 -*-

from tgspiders.crawler.environmental_data.crawler_all_enterprise.base import Base
from tgspiders.lib.post_root import qy_message
from pyquery import PyQuery as pq
from tgspiders.lib.log import Log
import time


class NXEmissionPicker(Base):
    def __init__(self):
        super(NXEmissionPicker, self).__init__('http://119.60.12.114:3000/xxgk')
        self.province_id = 64000000
        self.log = Log()

    def pick_autonomous_straight_enterprise(self):
        res_html = self.http.session.get('http://119.60.12.114:3000/xxgk/qyhjxxgk.html')
        cookie = 'JSESSIONID=' + res_html.cookies['JSESSIONID'] if res_html.ok else None

        if cookie is None:
            return

        res_html = self.http.session.get('http://119.60.12.114:3000/xxgk/qyhjxxgk.html',
     headers={'Host': '222.75.161.242:9000',
              'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Referer': 'http://119.60.12.114:3000/xxgk/qyhjxxgk!qyxq.action?qid=82fa3ecb3c1dab9c834a56674bc83ef7_5dba34d1429d287c',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              'Cookie': cookie}, timeout=600)
        html = res_html.text if res_html.ok else None

        if html is None:
            return

        lis = pq(html).find('#6400 ul').find('li')

        for i in range(0, lis.length):
            li = lis.eq(i)
            enterprise_href = li.find('a').attr('href')
            enterprise_infos = li.find('a').text()
            enterprise_infos = enterprise_infos.split('（')
            enterprise_name = enterprise_infos[0]
            enterprise_id = enterprise_infos[1].strip().lstrip().rstrip('）')
            res = dict({k: None for k in self.qy_style})
            res['qy_name'] = enterprise_name
            res['qy_id'] = enterprise_id
            res['province_id'] = self.province_id
            res['qy_url'] = 'http://119.60.12.114:3000' + enterprise_href
            res_html = self.http.session.get('http://119.60.12.114:3000' + enterprise_href,
                                             headers={'Host': '222.75.161.242:9000',
                                                      'Connection': 'keep-alive',
                                                      'Upgrade-Insecure-Requests': '1',
                                                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
                                                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                                      'Referer': 'http://119.60.12.114:3000/xxgk/qyhjxxgk.html',
                                                      'Accept-Encoding': 'gzip, deflate, sdch',
                                                      'Accept-Language': 'zh-CN,zh;q=0.8',
                                                      'Cookie': cookie},
                                             timeout=600)
            con_txt = res_html.text if res_html.ok else None

            if not con_txt:
                continue
            trs = pq(con_txt).find('#div1 table.table_edit').find('tr')
            jwd = trs.eq(2).find('td').eq(1).text().split('），纬度（')
            jd = jwd[0][3:]
            wd = jwd[1].strip().lstrip().rstrip('）')
            res['qy_wrylx'] = '废气'
            res['qy_jd'] = jd
            res['qy_wd'] = wd
            res['qy_address'] = trs.eq(1).find('td').eq(1).text()
            res['qy_corporation'] = trs.eq(0).find('td').eq(3).text()
            res['qy_industry'] = trs.eq(4).find('td').eq(1).text()
            res['qy_link_user'] = trs.eq(3).find('td').eq(1).text()
            res['qy_link_phone'] = trs.eq(3).find('td').eq(3).text()
            res['qy_introduce'] = trs.eq(7).find('td').eq(1).text()
            res['qy_link_email'] = trs.eq(6).find('td').eq(3).text()
            res['qy_fax'] = trs.eq(5).find('td').eq(3).text()
            self.log.logger.info(res)
            qy_message(res)

    def pick_ningdong_enterprise(self):
        res_html = self.http.session.get('http://119.60.0.59:20008/hb.portal.enterprise!list.sh',
                                         params={'indexMenu': '10.01.20'})
        cookie = 'JSESSIONID=' + res_html.cookies['JSESSIONID'] if res_html.ok else None

        if cookie is None:
            return

        res_html = self.http.session.get('http://119.60.0.59:20008/hb.portal.enterprise!right.sh',
                                         params={'panelMenu': '10.01.20'},
             headers={'Host': '119.60.0.59:20008',
                      'Connection': 'keep-alive',
                      'Upgrade-Insecure-Requests': '1',
                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                      'Referer': 'http://119.60.0.59:20008/hb.portal.enterprise!list.sh?indexMenu=10.01.20',
                      'Accept-Encoding': 'gzip, deflate, sdch',
                      'Accept-Language': 'zh-CN,zh;q=0.8',
                      'Cookie': cookie})

        html = res_html.text if res_html.ok else None

        if html is None:
            return

        lis = pq(html).find('.ddOneline2').find('A')

        for i in range(0, lis.length):
            li = lis.eq(i)
            enterprise_href = li.attr('href')
            enterprise_name = li.text().split(' [')[0]
            enterprise_id = li.find('SPAN').text()
            enterprise_id = enterprise_id[1: -1]
            res = dict({k: None for k in self.qy_style})
            res['qy_name'] = enterprise_name
            res['qy_id'] = enterprise_id
            res['province_id'] = self.province_id
            res['qy_url'] = 'http://119.60.0.59:20008/' + enterprise_href
            res_html = self.http.session.get('http://119.60.0.59:20008/' + enterprise_href,
         headers={'Host': '119.60.0.59:20008',
                  'Connection': 'keep-alive',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Referer': 'http://119.60.0.59:20008/hb.portal.enterprise!right.sh?panelMenu=10.01.20',
                  'Accept-Encoding': 'gzip, deflate, sdch',
                  'Accept-Language': 'zh-CN,zh;q=0.8',
                  'Cookie': cookie}, timeout=600)
            con_txt = res_html.text if res_html.ok else None

            if not con_txt:
                continue

            trs = pq(con_txt).find('table.table_edit').find('tr')
            jwd = trs.eq(2).find('td').eq(1).text().split('），纬度（')
            jd = jwd[0][3:]
            wd = jwd[1].strip().lstrip().rstrip('）')
            res['qy_jd'] = jd
            res['qy_wd'] = wd
            res['qy_address'] = trs.eq(1).find('td').eq(1).text()
            res['qy_corporation'] = trs.eq(0).find('td').eq(3).text()
            res['qy_industry'] = trs.eq(5).find('td').eq(1).text()
            res['qy_link_user'] = trs.eq(3).find('td').eq(1).text()
            res['qy_link_phone'] = trs.eq(3).find('td').eq(3).text()
            res['qy_introduce'] = trs.eq(6).find('td').eq(1).text()
            res['qy_link_email'] = trs.eq(4).find('td').eq(1).text()

    def pick_shizuishan_enterprise(self):
        res_html = self.http.session.get('http://218.95.153.246:9002/xxgk/qyhjxxgk.html')
        cookie = 'JSESSIONID=' + res_html.cookies['JSESSIONID'] if res_html.ok else None

        if cookie is None:
            return

        res_html = self.http.session.get('http://218.95.153.246:9002/xxgk/qyhjxxgk.html',
     headers={
         'Accept': 'image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*',
         'Referer': 'http://218.95.153.246:9002/xxgk/qyhjxxgk.html',
         'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.5',
         'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; InfoPath.3; Tablet PC 2.0)',
         'Accept-Encoding': 'gzip, deflate',
         'Host': '218.95.153.246:9002',
         'Connection': 'Keep-Alive',
         'Cookie': cookie})

        html = res_html.text if res_html.ok else None

        if html is None:
            return

        lis = pq(html).find('ul#psarea2').find('li')

        for i in range(1, lis.length):
            li = lis.eq(i)
            enterprise_href = li.find('div.title').find('a').attr('href')
            enterprise_name = li.find('div.title').find('a').text()
            enterprise_id = li.find('div.pscode').text()
            res = dict({k: None for k in self.qy_style})
            res['qy_name'] = enterprise_name
            res['qy_id'] = enterprise_id
            res['province_id'] = self.province_id
            res['qy_url'] = 'http://218.95.153.246:9002' + enterprise_href
            res_html = self.http.session.get('http://218.95.153.246:9002' + enterprise_href,
         headers={'Host': '218.95.153.246:9002',
                  'Connection': 'keep-alive',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Referer': 'http://218.95.153.246:9002/xxgk/qyhjxxgk.html',
                  'Accept-Encoding': 'gzip, deflate, sdch',
                  'Accept-Language': 'zh-CN,zh;q=0.8',
                  'Cookie': cookie}, timeout=600)
            con_txt = res_html.text if res_html.ok else None

            if not con_txt:
                continue

            trs = pq(con_txt).find('table.table_edit').find('tr')
            jwd = trs.eq(2).find('td').eq(1).text().split('），纬度（')
            jd = jwd[0][3:]
            wd = jwd[1].strip().lstrip().rstrip('）')
            res['qy_wrylx'] = '废气'
            res['qy_jd'] = jd
            res['qy_wd'] = wd
            res['qy_address'] = trs.eq(1).find('td').eq(1).text()
            res['qy_corporation'] = trs.eq(0).find('td').eq(3).text()
            res['qy_industry'] = trs.eq(4).find('td').eq(1).text()
            res['qy_link_user'] = trs.eq(3).find('td').eq(1).text()
            res['qy_link_phone'] = trs.eq(3).find('td').eq(3).text()
            res['qy_fax'] = trs.eq(5).find('td').eq(3).text()
            res['qy_introduce'] = trs.eq(7).find('td').eq(1).text()
            res['qy_link_email'] = trs.eq(6).find('td').eq(3).text()
            res['qy_link_phone'] = res['qy_link_phone'] + ',' + trs.eq(3).find('td').eq(3).text() if trs.eq(6).find(
                'td').eq(1).text() is not None else res['qy_link_phone']

    def pick_yinchuan_enterprise(self):
        res_html = self.http.session.get('http://119.60.9.17:9001/xxgk/qyhjxxgk.html')
        cookie = 'JSESSIONID=' + res_html.cookies['JSESSIONID'] if res_html.ok else None

        if cookie is None:
            return

        res_html = self.http.session.get('http://119.60.9.17:9001/xxgk/qyhjxxgk.html',
         headers={'Host': '119.60.9.17:9001',
                  'Connection': 'keep-alive',
                  'Cache-Control': 'max-age=0',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Accept-Encoding': 'gzip, deflate, sdch',
                  'Accept-Language': 'zh-CN,zh;q=0.8',
                  'Cookie': cookie})

        html = res_html.text if res_html.ok else None

        if html is None:
            return

        lis = pq(html).find('ul#psarea2').find('li')

        for i in range(1, lis.length):
            li = lis.eq(i)
            enterprise_href = li.find('div.title').find('a').attr('href')
            enterprise_name = li.find('div.title').find('a').text()
            enterprise_id = li.find('div.pscode').text()
            res = dict({k: None for k in self.qy_style})
            res['qy_name'] = enterprise_name
            res['qy_id'] = enterprise_id
            res['province_id'] = self.province_id
            res['qy_url'] = 'http://119.60.9.17:9001' + enterprise_href
            res_html = self.http.session.get('http://119.60.9.17:9001' + enterprise_href,
             headers={'Host': '119.60.9.17:9001',
                      'Connection': 'keep-alive',
                      'Upgrade-Insecure-Requests': '1',
                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                      'Referer': 'http://119.60.9.17:9001/xxgk/qyhjxxgk.html',
                      'Accept-Encoding': 'gzip, deflate, sdch',
                      'Accept-Language': 'zh-CN,zh;q=0.8',
                      'Cookie': cookie}, timeout=600)
            con_txt = res_html.text if res_html.ok else None

            if not con_txt:
                continue

            trs = pq(con_txt).find('table.table_edit').find('tr')
            jwd = trs.eq(2).find('td').eq(1).text().split('），纬度（')
            jd = jwd[0][3:]
            wd = jwd[1].strip().lstrip().rstrip('）')
            res['qy_wrylx'] = '废气'
            res['qy_jd'] = jd
            res['qy_wd'] = wd
            res['qy_address'] = trs.eq(1).find('td').eq(1).text()
            res['qy_corporation'] = trs.eq(0).find('td').eq(3).text()
            res['qy_industry'] = trs.eq(4).find('td').eq(1).text()
            res['qy_link_user'] = trs.eq(3).find('td').eq(1).text()
            res['qy_link_phone'] = trs.eq(3).find('td').eq(3).text()
            res['qy_fax'] = trs.eq(5).find('td').eq(3).text()
            res['qy_introduce'] = trs.eq(7).find('td').eq(1).text()
            res['qy_link_email'] = trs.eq(6).find('td').eq(3).text()
            res['qy_link_phone'] = res['qy_link_phone'] + ',' + trs.eq(3).find('td').eq(3).text() if trs.eq(6).find(
                'td').eq(1).text() is not None else res['qy_link_phone']
            # self.insert(res)

    def pick_zhongwei_enterprise(self):
        res_html = self.http.session.get('http://222.75.161.242:9005/xxgk/qyhjxxgk.html')
        cookie = 'JSESSIONID=' + res_html.cookies['JSESSIONID'] if res_html.ok else None

        if cookie is None:
            return

        res_html = self.http.session.get('http://222.75.161.242:9005/xxgk/qyhjxxgk.html',
         headers={'Host': '222.75.161.242:9005',
                  'Connection': 'keep-alive',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Referer': 'http://222.75.161.242:9005/xxgk/qyhjxxgk.html',
                  'Accept-Encoding': 'gzip, deflate, sdch',
                  'Accept-Language': 'zh-CN,zh;q=0.8',
                  'Cookie': cookie})

        html = res_html.text if res_html.ok else None

        if html is None:
            return

        lis = pq(html).find('ul#psarea2').find('li')

        for i in range(1, lis.length):
            li = lis.eq(i)
            enterprise_href = li.find('div.title').find('a').attr('href')
            enterprise_name = li.find('div.title').find('a').text()
            enterprise_id = li.find('div.pscode').text()
            res = dict({k: None for k in self.qy_style})
            res['qy_name'] = enterprise_name
            res['qy_id'] = enterprise_id
            res['province_id'] = self.province_id
            res['qy_url'] = 'http://222.75.161.242:9005' + enterprise_href
            res_html = self.http.session.get('http://222.75.161.242:9005' + enterprise_href,
         headers={'Host': '222.75.161.242:9005',
                  'Connection': 'keep-alive',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Referer': 'http://222.75.161.242:9005/xxgk/qyhjxxgk.html',
                  'Accept-Encoding': 'gzip, deflate, sdch',
                  'Accept-Language': 'zh-CN,zh;q=0.8',
                  'Cookie': cookie}, timeout=600)
            con_txt = res_html.text if res_html.ok else None

            if not con_txt:
                continue

            trs = pq(con_txt).find('table.table_edit').find('tr')
            jwd = trs.eq(2).find('td').eq(1).text().split('），纬度（')
            jd = jwd[0][3:]
            wd = jwd[1].strip().lstrip().rstrip('）')
            res['qy_wrylx'] = '废气'
            res['qy_jd'] = jd
            res['qy_wd'] = wd
            res['qy_address'] = trs.eq(1).find('td').eq(1).text()
            res['qy_corporation'] = trs.eq(0).find('td').eq(3).text()
            res['qy_industry'] = trs.eq(4).find('td').eq(1).text()
            res['qy_link_user'] = trs.eq(3).find('td').eq(1).text()
            res['qy_link_phone'] = trs.eq(3).find('td').eq(3).text()
            res['qy_fax'] = trs.eq(5).find('td').eq(3).text()
            res['qy_introduce'] = trs.eq(7).find('td').eq(1).text()
            res['qy_link_email'] = trs.eq(6).find('td').eq(3).text()
            res['qy_link_phone'] = res['qy_link_phone'] + ',' + trs.eq(3).find('td').eq(3).text() if trs.eq(6).find(
                'td').eq(1).text() is not None else res['qy_link_phone']
            # self.insert(res)

    # @retry
    def pick_wuzhong_enterprise(self):
        res_html = self.http.session.get('http://222.75.161.242:9003/xxgk/qyhjxxgk.html')
        cookie = 'JSESSIONID=' + res_html.cookies['JSESSIONID'] if res_html.ok else None

        if cookie is None:
            return

        res_html = self.http.session.get('http://222.75.161.242:9003/xxgk/qyhjxxgk.html',
         headers={'Host': '222.75.161.242:9003',
                  'Connection': 'keep-alive',
                  'Upgrade-Insecure-Requests': '1',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Referer': 'http://222.75.161.242:9003/xxgk/qyhjxxgk.html',
                  'Accept-Encoding': 'gzip, deflate, sdch',
                  'Accept-Language': 'zh-CN,zh;q=0.8',
                  'Cookie': cookie})

        html = res_html.text if res_html.ok else None

        if html is None:
            return

        for l in range(1, 4):

            lis = pq(html).find('ul#psarea' + str(l) + '2').find('li')

            for i in range(1, lis.length):
                li = lis.eq(i)
                enterprise_href = li.find('div.title').find('a').attr('href')
                enterprise_name = li.find('div.title').find('a').text()
                enterprise_id = li.find('div.pscode').text()
                res = dict({k: None for k in self.qy_style})
                res['qy_name'] = enterprise_name
                res['qy_id'] = enterprise_id
                res['province_id'] = self.province_id
                res['qy_url'] = 'http://222.75.161.242:9003' + enterprise_href
                res_html = self.http.session.get('http://222.75.161.242:9003' + enterprise_href,
             headers={'Host': '222.75.161.242:9003',
                      'Connection': 'keep-alive',
                      'Upgrade-Insecure-Requests': '1',
                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                      'Referer': 'http://222.75.161.242:9003/xxgk/qyhjxxgk.html',
                      'Accept-Encoding': 'gzip, deflate, sdch',
                      'Accept-Language': 'zh-CN,zh;q=0.8',
                      'Cookie': cookie}, timeout=600)
                con_txt = res_html.text if res_html.ok else None

                if not con_txt:
                    continue

                trs = pq(con_txt).find('table.table_edit').find('tr')
                jwd = trs.eq(2).find('td').eq(1).text().split('），纬度（')
                jd = jwd[0][3:]
                wd = jwd[1].strip().lstrip().rstrip('）')
                res['qy_wrylx'] = '废气'
                res['qy_jd'] = jd
                res['qy_wd'] = wd
                res['qy_address'] = trs.eq(1).find('td').eq(1).text()
                res['qy_corporation'] = trs.eq(0).find('td').eq(3).text()
                res['qy_industry'] = trs.eq(4).find('td').eq(1).text()
                res['qy_link_user'] = trs.eq(3).find('td').eq(1).text()
                res['qy_link_phone'] = trs.eq(3).find('td').eq(3).text()
                res['qy_fax'] = trs.eq(5).find('td').eq(3).text()
                res['qy_introduce'] = trs.eq(7).find('td').eq(1).text()
                res['qy_link_email'] = trs.eq(6).find('td').eq(3).text()
                res['qy_link_phone'] = res['qy_link_phone'] + ',' + trs.eq(3).find('td').eq(3).text() if trs.eq(6).find(
                    'td').eq(1).text() is not None else res['qy_link_phone']
                # self.insert(res)

    # @retry
    def pick_guyuan_enterprise(self):
        res_html = self.http.session.get('http://222.75.161.242:9004/xxgk/qyhjxxgk.html')
        cookie = 'JSESSIONID=' + res_html.cookies['JSESSIONID'] if res_html.ok else None

        if cookie is None:
            return

        res_html = self.http.session.get('http://222.75.161.242:9004/xxgk/qyhjxxgk.html',
             headers={'Host': '222.75.161.242:9004',
                      'Connection': 'keep-alive',
                      'Upgrade-Insecure-Requests': '1',
                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                      'Referer': 'http://222.75.161.242:9004/xxgk/qyhjxxgk.html',
                      'Accept-Encoding': 'gzip, deflate, sdch',
                      'Accept-Language': 'zh-CN,zh;q=0.8',
                      'Cookie': cookie})

        html = res_html.text if res_html.ok else None

        if html is None:
            return

        lis = pq(html).find('ul#psarea2').find('li')

        for i in range(1, lis.length):
            li = lis.eq(i)
            enterprise_href = li.find('div.title').find('a').attr('href')
            enterprise_name = li.find('div.title').find('a').text()
            enterprise_id = li.find('div.pscode').text()
            res = dict({k: None for k in self.qy_style})
            res['qy_name'] = enterprise_name
            res['qy_id'] = enterprise_id
            res['province_id'] = self.province_id
            res['qy_url'] = 'http://222.75.161.242:9004' + enterprise_href
            res_html = self.http.session.get('http://222.75.161.242:9004' + enterprise_href,
             headers={'Host': '222.75.161.242:9004',
                      'Connection': 'keep-alive',
                      'Upgrade-Insecure-Requests': '1',
                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                      'Referer': 'http://222.75.161.242:9004/xxgk/qyhjxxgk.html',
                      'Accept-Encoding': 'gzip, deflate, sdch',
                      'Accept-Language': 'zh-CN,zh;q=0.8',
                      'Cookie': cookie},
             timeout=600)
            con_txt = res_html.text if res_html.ok else None

            if not con_txt:
                continue

            trs = pq(con_txt).find('table.table_edit').find('tr')
            jwd = trs.eq(2).find('td').eq(1).text().split('），纬度（')
            jd = jwd[0][3:]
            wd = jwd[1].strip().lstrip().rstrip('）')
            res['qy_wrylx'] = '废气'
            res['qy_jd'] = jd
            res['qy_wd'] = wd
            res['qy_address'] = trs.eq(1).find('td').eq(1).text()
            res['qy_corporation'] = trs.eq(0).find('td').eq(3).text()
            res['qy_industry'] = trs.eq(4).find('td').eq(1).text()
            res['qy_link_user'] = trs.eq(3).find('td').eq(1).text()
            res['qy_link_phone'] = trs.eq(3).find('td').eq(3).text()
            res['qy_fax'] = trs.eq(5).find('td').eq(3).text()
            res['qy_introduce'] = trs.eq(7).find('td').eq(1).text()
            res['qy_link_email'] = trs.eq(6).find('td').eq(3).text()
            res['qy_link_phone'] = res['qy_link_phone'] + ',' + trs.eq(3).find('td').eq(3).text() if trs.eq(6).find(
                'td').eq(1).text() is not None else res['qy_link_phone']
            # self.insert(res)

    def pick_all(self):
        self.log.logger.info('开始获取宁夏企业信息')
        self.pick_autonomous_straight_enterprise()
        # self.pick_ningdong_enterprise()
        # self.pick_shizuishan_enterprise()
        # self.pick_yinchuan_enterprise()   #可以
        # self.pick_zhongwei_enterprise()
        # self.pick_wuzhong_enterprise()  #keyi 
        # self.pick_guyuan_enterprise()

if __name__ == '__main__':
    t = time.time()
    nx = NXEmissionPicker()
    nx.pick_all()

    print('time----------------->', time.time() - t)
