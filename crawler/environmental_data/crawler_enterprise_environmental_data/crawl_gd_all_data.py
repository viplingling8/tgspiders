# coding:utf-8

from tgspiders.lib.post_root import qy_decetion, get_qy_id_url_lasttime
from concurrent.futures import ThreadPoolExecutor
from tgspiders.lib.float_util import float_cast
from datetime import datetime, timedelta
from tgspiders.lib.log import Log
import requests
import json
import math
import time
import re


class CrawlGdEnvData():
    """docstring for CrawlGdEnvData"""

    def __init__(self):
        super(CrawlGdEnvData, self).__init__()
        self.log = Log()
        self.session = requests.Session()
        self.province_id = 44000000
        self.sql_type = ['province_id', 'enterprise_id', 'monitor_point',
                         'monitor_time', 'project_id', 'monitor_value',
                         'standard_limit_value', 'evaluation_criterion']

    def get_all_qyurl_by_provinceid(self, province_id, qy_style):

        list_qy = get_qy_id_url_lasttime(province_id, qy_style)
        # qy_info = dict()
        qy_info = {k['qyid']: k['qyname'] for k in list_qy}
        # qy_info = {'ad8a9bd8-4074-11e3-a6a2-6c626d51ef74': '湛江中粤能源有限公司', 'ad36a9b1-4074-11e3-a6a2-6c626d51ef74': '广东粤电靖海发电有限公司'}
        return qy_info

    def crawl(self):
        self.log.logger.info('开始获取广东环保数据')
        qy_dict = self.get_all_qyurl_by_provinceid(self.province_id, 1)
        print('qy_dict--------->', qy_dict)
        for qy_id, qy_name in qy_dict.items():
            self.crawl_qy(qy_id, qy_name)

        # with ThreadPoolExecutor(10) as executor:
        #     for qy_id, qy_name in qy_dict.items():
        #         executor.submit(self.crawl_qy, qy_id, qy_name)

    def crawl_qy(self, qy_id, qy_name):
        patten = re.compile(r'var optionmplist = \$\("<option value=\'(.*)\' >(.*)</option>"\);', re.IGNORECASE)
        url = 'https://app.gdep.gov.cn/epinfo/selfmonitor/getSelfmonitorMonitor/%s?ename=%s&year=%s' % \
              (qy_id, qy_name, datetime.now().year)
        print('=============>', url)
        r = self.session.get(url)

        if r.ok:
            res = patten.findall(r.text)
            unit_options = {item[0]: item[1] for item in res}
            start_time = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
            end_time = datetime.now().strftime('%Y-%m-%d')

            for mp_id, unit_name in unit_options.items():
                type_data = self.get_miinfo(mp_id)
                type_options = {item['miid']: item['miname'] for item in json.loads(type_data) if item['mitec'] == '2'}

                for mi_id, type_name in type_options.items():
                    res = self.crawl_page(mp_id, mi_id, start_time, end_time, type_name, qy_id,
                                          str(datetime.now().year))

                    if res:
                        res = json.loads(res)

                        if 'totel' in res:
                            total = int(res['totel'])

                            self.pick_data(res, qy_id, unit_name, type_name)

                            for i in range(1, math.ceil(total / 24) + 1):
                                res = self.crawl_page(mp_id, mi_id, start_time, end_time, type_name, qy_id,
                                                      str(datetime.now().year), i)
                                self.pick_data(json.loads(res), qy_id, unit_name, type_name)

    def pick_data(self, data, qy_id, unit_name, type_name):
        if isinstance(data, dict) and 'results' in data:
            for item in data['results']:
                res = dict({k: None for k in self.sql_type})
                res['province_id'] = self.province_id
                res['enterprise_id'] = qy_id
                res['monitor_point'] = unit_name
                res['monitor_time'] = item['monitortime']

                res['project_id'] = type_name
                res['monitor_value'] = float_cast(item['monitorValue'], None)
                limit_value = item['standardvalue'].split('-')
                res['standard_limit_value'] = float_cast(limit_value[1]) if len(limit_value) > 1 else None
                res['evaluation_criterion'] = item['invalidreason'] if 'invalidreason' in item else None
                self.log.logger.info(res)
                qy_decetion(res)

    def get_miinfo(self, mp_id):
        r = self.session.post('https://app.gdep.gov.cn/epinfo/selfmonitor/findMiinfo', data={'mpid': mp_id})
        return r.text if r.ok else None

    def crawl_page(self, mp_id, mi_id, start_time, end_time, miinfoname, qy_id, year, page=None):
        data = {
            'mpId': mp_id,
            'miId': mi_id,
            'startime': start_time,
            'endtime': end_time,
            'miinfoname': miinfoname,
            'directid': qy_id,
            'id': qy_id,
            'year': year,
        }

        if page:
            data['page'] = page

        r = self.session.post('https://app.gdep.gov.cn/epinfo/selfmonitor/findOM3', data=data)

        return r.text if r.ok else None


def main():
    cgd = CrawlGdEnvData()
    cgd.crawl()


if __name__ == '__main__':
    main()
    # start_time = time.time()
    # cgd = CrawlGdEnvData()
    # cgd.crawl()
    # print('long --------------->', time.time() - start_time)
