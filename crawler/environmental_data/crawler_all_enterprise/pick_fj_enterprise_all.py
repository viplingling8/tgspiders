# -*- encoding= utf-8 -*-

from tgspiders.crawler.environmental_data.crawler_all_enterprise.base import Base
from tgspiders.lib.post_root import qy_message
from pyquery import PyQuery as pq
from tgspiders.lib.log import Log
import time


class FJEmissionPicker(Base):
    def __init__(self):
        super(FJEmissionPicker, self).__init__('http://wryfb.fjemc.org.cn/')
        self.province_id = 35000000
        self.log = Log()
        self.href = 'http://wryfb.fjemc.org.cn/'

    def pick_enter_info(self, qy_url):
        try:
            enp_html = self.http.session.get(qy_url,
                                             headers={"Host": "wryfb.fjemc.org.cn",
                                                      "Connection": "keep-alive",
                                                      "Cache-Control": "max-age=0",
                                                      "Upgrade-Insecure-Requests": "1",
                                                      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36",
                                                      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                                                      "Accept-Encoding": "gzip, deflate, sdch",
                                                      "Accept-Language": "zh-CN,zh;q=0.8"},
                                             timeout=600)
            return enp_html.text if enp_html.ok else None
        except:
            return None

    def pick_citys_href(self):

        citys = ['中海福建燃气发电有限公司', '东亚电力（厦门）有限公司', '福建晋江天然气发电有限公司', '华能国际电力股份有限公司福州电厂', '福州红庙岭垃圾焚烧发电有限公司', '福州天楹环保能源有限公司',
                 '厦门华夏国际电力发展有限公司', '厦门同集热电有限公司', '福建省鸿山热电有限责任公司', '福建清源科技有限公司', '福建省石狮热电有限责任公司', '石狮市鸿峰环保生物工程有限公司',
                 '华阳电业有限公司', '福建华电永安发电有限公司', '福建大唐国际宁德发电有限责任公司', '福建晋江热电有限公司', '漳浦龙口热电厂', '国电泉州热电有限公司', '国电福州发电有限公司',
                 '福建华电可门发电有限公司', '厦门海翼杏林热电有限公司', '厦门瑞新热电有限公司', '莆田市圣元环保电力有限公司', '南安市圣元环保电力有限公司']
        enterInfos = []

        for city in citys:
            url = 'http://wryfb.fjemc.org.cn/seach.aspx?name=%s&area_id=&type=1' % (city,)
            res_html = self.http.session.get(url)
            con_txt = str(res_html.text) if res_html.ok else None

            if con_txt is None:
                return None

            a = pq(con_txt).find('.tr1 td a')
            enterInfo = {}
            enterInfo["enterHref"] = a.attr('href')
            enterInfo["enterId"] = enterInfo["enterHref"].split('id=')[1]
            enterInfo["enterName"] = a.text()
            enterInfos.append(enterInfo)
        return enterInfos

    def pick_all(self):
        self.log.logger.info('开始获取福建企业信息')
        enp_data_lists = self.pick_citys_href()

        for enp in enp_data_lists:
            # print(enp)
            res = dict({k: None for k in self.qy_style})
            res['qy_name'] = enp['enterName']
            res['qy_id'] = enp['enterId']
            res['province_id'] = self.province_id
            res['qy_url'] = self.href + enp['enterHref']
            qy_txt = self.pick_enter_info(res['qy_url'])

            if qy_txt is None:
                continue

            res['qy_url'] = res['qy_url'].replace('page0.aspx?', 'page7.aspx?')
            trs = pq(pq(qy_txt).html()).find('table.table2').find('tr')

            res['qy_industry'] = trs.eq(1).find('td').eq(1).text()
            res['qy_corporation'] = trs.eq(2).find('td').eq(1).text()
            res['qy_scale'] = trs.eq(4).find('td').eq(1).text()
            res['qy_register_type'] = trs.eq(5).find('td').eq(1).text()
            res['qy_link_phone'] = trs.eq(7).find('td').eq(1).text()
            res['qy_fax'] = trs.eq(8).find('td').eq(1).text()
            res['qy_address'] = trs.eq(10).find('td').eq(1).text()
            self.log.logger.info(res)
            qy_message(res)


if __name__ == '__main__':
    t = time.time()
    fj = FJEmissionPicker()
    fj.pick_all()

    print('time----------------->', time.time() - t)
