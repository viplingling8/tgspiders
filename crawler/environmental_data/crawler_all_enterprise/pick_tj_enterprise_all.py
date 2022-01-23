# -*- coding: utf-8 -*-

from tgspiders.crawler.environmental_data.crawler_all_enterprise.base import Base
from tgspiders.lib.post_root import qy_message
from pyquery import PyQuery as pq
from tgspiders.lib.log import Log
import time


class TJEmissionPicker(Base):
    def __init__(self):
        super(TJEmissionPicker, self).__init__('http://60.30.64.234:90/tj-monitor-pub/text_result.do')
        self.province_id = 12000000
        self.log = Log()
        self.href = 'http://60.30.64.234:90'

    def pick_enter_infos(self, cookie):

        try:
            enterInfos = []
            pageNum = 1

            while(pageNum < 38):
                res_html = self.http.session.post('http://60.30.64.234:90/tj-monitor-pub/text_result.do',
                      headers={'Accept': 'image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*',
                                'Referer': 'http://60.30.64.234:90/tj-monitor-pub/text_result.do',
                                'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.5',
                                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; Touch; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; Tablet PC 2.0)',
                                'Content-Type': 'application/x-www-form-urlencoded',
                                'Accept-Encoding': 'gzip, deflate',
                                'Content-Length': '35',
                                'Host': '60.30.64.234:90',
                                'Connection': 'Keep-Alive',
                                'Pragma': 'no-cache',
                                'Cookie':  cookie},
                     data={'type_id': '2',
                            'orgName': '',
                            'area': '',
                            'pageIndex': pageNum},
                      timeout=600)
                const = res_html.text if res_html.ok else None

                if const is None:
                    return None

                lis = pq(const).find('div.search_list ul').find('li')

                for i in range(0, lis.length):
                    a = pq(lis.eq(i).find('a').eq(0))
                    enterInfo = {}
                    enterInfo["href"] = a.attr('href')
                    enterInfo["id"] = str(self.province_id) + '-' + enterInfo["href"].split('org_jbxx/')[1].replace('.do', '')
                    enterInfo["name"] = a.text()
                    enterInfos.append(enterInfo)

                pageNum += 1

            return enterInfos
        except:
            return None

    def pick_enter_info(self, enp_href, cookie):
        try:
            enp_html = self.http.session.get(self.href + enp_href,
                                             headers={'Accept': 'image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*',
                                                 'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.5',
                                                 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; Touch; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; Tablet PC 2.0)',
                                                 'Accept-Encoding': 'gzip, deflate',
                                                 'Host': '60.30.64.234:90',
                                                 'Connection': 'Keep-Alive',
                                                 'Cookie': cookie},
                                             timeout=600)
            return enp_html.text if enp_html.ok else None
        except:
            return None

    def pick_all(self):
        self.log.logger.info('开始获取天津企业信息')
        res_html = self.http.session.get('http://60.30.64.234:90/tj-monitor-pub/text_result.do')
        cookie = 'JSESSIONID=' + res_html.cookies['JSESSIONID'] if res_html.ok else None

        if cookie is None:
            return

        enp_list = self.pick_enter_infos(cookie)

        for enp in enp_list:
            enp_href = enp['href']

            con_txt = self.pick_enter_info(enp_href, cookie)

            if con_txt is None:
                continue
            trs = pq(pq(con_txt).html()).find('div.com_prof').find('table').find('tr')

            res = dict({k: None for k in self.qy_style})
            res['qy_name'] = enp['name']
            # print("res['qy_name']---------", res['qy_name'])
            res['qy_id'] = enp['id']
            res['province_id'] = self.province_id
            res['qy_city'] = '天津'
            res['qy_city_id'] = self.province_id
            res['qy_url'] = self.href + enp_href.replace('/org_jbxx/', '/org_zdjc/')
            res['qy_introduce'] = pq(pq(con_txt).html()).find('div.com_desc').text()
            res['qy_wrylx'] = trs.eq(0).find('td').eq(3).text()
            res['qy_organization_code'] = trs.eq(1).find('td').eq(1).text()
            res['qy_address'] = trs.eq(1).find('td').eq(3).text()
            res['qy_jd'] = trs.eq(2).find('td').eq(1).text()
            res['qy_wd'] = trs.eq(2).find('td').eq(3).text()
            res['qy_corporation'] = trs.eq(3).find('td').eq(1).text()
            res['qy_industry'] = trs.eq(3).find('td').eq(3).text()
            res['qy_link_user'] = trs.eq(4).find('td').eq(1).text()
            res['qy_link_phone'] = trs.eq(4).find('td').eq(3).text()
            res['qy_auto_monitor_style'] = trs.eq(5).find('td').eq(1).text()
            res['qy_auto_monitor_operation_style'] = trs.eq(6).find('td').eq(1).text()
            # self.insert(res)
            self.log.logger.info(res)
            qy_message(res)

if __name__ == '__main__':
    t = time.time()
    tj = TJEmissionPicker()
    tj.pick_all()
    print('time----------------->', time.time() - t)
