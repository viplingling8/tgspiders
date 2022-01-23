# -*- coding: utf-8 -*-

from tgspiders.crawler.environmental_data.crawler_enterprise_environmental_data.base import Base
from tgspiders.lib.post_root import qy_decetion, get_qy_id_url_lasttime
from tgspiders.lib.float_util import float_cast
from pyquery import PyQuery as pq
from tgspiders.lib.log import Log
from datetime import datetime
import calendar
import time


class HEEmissionPickerData(Base):
    def __init__(self):
        super(HEEmissionPickerData, self).__init__('http://121.28.49.84:8003/')
        self.province_id = 13000000
        self.log = Log()

    def get_all_qyname_by_provinceid(self, province_id, qy_style):
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

    def pick_dev_data(self, datas, header):

        try:
            res_html = self.http.session.post('http://121.28.49.84:8003/',
                                              data=datas,
                                              headers=header,
                                              timeout=600)
            return res_html.text if res_html.ok else None

        except Exception as e:
            self.log.logger.info(e)
            return None

    def insert_dev_datas(self, dev_datas, qy_id):
        dev_list = ['东厂12至15号脱硫后总出口', '1号脱销A侧出口', '1号脱销B侧出口', '2号A侧脱销排口', '2号B侧脱销排口', '12号脱硫排口']
        qy_list = ['tvsitet161', 'tvsitet183', 'tvsitet186', 'tvsitet260']
        trs = pq(dev_datas).find('table').find('tr')
        nowStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        nowDate = self.parser.set_date(nowStr).set_time(nowStr).datetime

        if trs.length < 3:
            return

        for i in range(2, trs.length):
            tds = trs.eq(i).find('td')
            dev_name = tds.eq(3).text()

            if qy_id in qy_list:
                dev_name = dev_name + '1'

            if qy_id == 'tvsitet101' and dev_name == '废气排放口':
                dev_name = dev_name + '1'

            timeStr = tds.eq(1).text() + ':00:00'
            timeDate = self.parser.set_date(timeStr).set_time(timeStr).datetime

            if timeDate > nowDate:
                continue

            res = dict({k: None for k in self.sql_type})
            res['province_id'] = self.province_id
            res['enterprise_id'] = qy_id
            res['monitor_point'] = dev_name
            res['monitor_time'] = str(timeDate)
            res['project_id'] = tds.eq(2).text()
            res['monitor_value'] = float_cast(tds.eq(4).text()) if tds.eq(4).text() != '' else None
            res['standard_limit_value'] = float_cast(
                tds.eq(7).text().replace('<', '').replace('=', '')) if float_cast(
                tds.eq(7).text().replace('<', '').replace('=', '')) > 0 else None
            res['evaluation_criterion'] = tds.eq(8).text()
            qy_decetion(res)
            self.log.logger.info(res)

    def get_months(self, start_date, end_date):
        start_year = start_date.strftime('%Y')
        end_year = end_date.strftime('%Y')
        years = int(end_year) - int(start_year)
        start_month = start_date.strftime('%m')
        end_month = end_date.strftime('%m')
        months = int(end_month) + 12 * years - int(start_month)

        return months

    def get_enperprise_btn_query(self, new_datas, header):
        try:
            r = self.http.session.post('http://121.28.49.84:8003/',
                                       data=new_datas,
                                       headers=header,
                                       timeout=120)
            con_txt = r.text if r.ok else None

            if con_txt is None:
                return None

            con_list = con_txt.split('|')
            index_viewstate = con_list.index('__VIEWSTATE')
            index_eventvalidation = con_list.index('__EVENTVALIDATION')
            index_tvsite_expandstate = con_list.index('tvsite_ExpandState')

            if index_viewstate < 0 or index_eventvalidation < 0 or index_tvsite_expandstate < 0:
                return None

            new_datas['__VIEWSTATE'] = con_list[index_viewstate + 1]
            new_datas['__EVENTVALIDATION'] = con_list[index_eventvalidation + 1]
            new_datas['tvsite_ExpandState'] = con_list[index_tvsite_expandstate + 1]

            citys = pq(con_txt).find('table')

            for i in range(0, citys.length):
                tds = citys.eq(i).find('tr').eq(0).find('td')

                if tds is None or tds.length < 4:
                    continue

                a_texts = tds.eq(3).find('a')

                if a_texts is None:
                    continue

                if a_texts.text() != new_datas['txt_EnpName']:
                    continue

                enp_node = a_texts.attr('onclick').split("'")[1]
                enp_id = a_texts.attr('href').split("'")[3]
                enp_id = enp_id.replace('\\\\', '\\')
                new_datas['tvsite_SelectedNode'] = enp_node
                new_datas['__EVENTARGUMENT'] = enp_id
                return new_datas

        except Exception as e:
            self.log.logger.info(e)
            return None

    def get_enperprise_tvsitet(self, new_datas_select, header):
        try:
            r = self.http.session.post('http://121.28.49.84:8003/',
                                       data=new_datas_select,
                                       headers=header,
                                       timeout=120)
            con_txt = r.text if r.ok else None

            if con_txt is None:
                return None

            con_list = con_txt.split('|')
            index_viewstate = con_list.index('__VIEWSTATE')
            index_eventvalidation = con_list.index('__EVENTVALIDATION')

            if index_viewstate < 0 or index_eventvalidation < 0:
                return None

            new_datas = new_datas_select.copy()
            new_datas['__VIEWSTATE'] = con_list[index_viewstate + 1]
            new_datas['__EVENTVALIDATION'] = con_list[index_eventvalidation + 1]

            return new_datas
        except Exception as e:
            self.log.logger.info(e)
            return None

    def get_datas(self):
        res_html = self.http.session.get('http://121.28.49.84:8003/')
        html = res_html.text if res_html.ok else None

        if html is None:
            return

        data_keys = ['ScriptManager1', 'ddl_year', 'txt_EnpName', 'rd_DataType', 'txtStartDate_autoData',
                     'txtEndDate_autoData', 'rd_SiteType', 'txtStartDate_handData', 'txtEndDate_handData',
                     'txtStartDate_NoiseData', 'txtStartDate_otherData', 'txtEndDate_otherData', 'txt_reason',
                     'txt_reason_end', 'txt_monplan', 'txtyearreport', 'ddl_city', 'txt_monplan_sum',
                     'Asp_MonPlan_Sum_input', '__EVENTTARGET', '__EVENTARGUMENT', '__LASTFOCUS', '__VIEWSTATE',
                     '__EVENTVALIDATION', 'tvsite_ExpandState', 'tvsite_SelectedNode', 'tvsite_PopulateLog',
                     '__ASYNCPOST', 'Asp_AutoData_input', 'Asp_HandData_input', 'Asp_NoiseData_input']
        inputs = pq(html).find('body').find('input')
        datas = {k: '' for k in data_keys}

        for i in range(0, inputs.length):
            input = inputs.eq(i)
            name = input.attr('name')
            value = input.val()

            if name in data_keys:
                datas[name] = value if value else ''

        datas['__ASYNCPOST'] = 'true'
        datas['ScriptManager1'] = 'UpdatePanel1|btn_Query'
        datas['ddl_year'] = '2018'
        datas['rd_DataType'] = '1'
        datas['rd_SiteType'] = '1'
        datas['tvsite_ExpandState'] = 'ennnnnnnnnnnnnnn'
        return datas

    def pick_data(self, qy_infos, header):
        datas = self.get_datas()

        for qy_info in qy_infos:
            qy_id = qy_info['qy_id']
            qy_name = qy_info['qy_name']
            datas['txt_EnpName'] = qy_name
            new_datas_select = self.get_enperprise_btn_query(datas.copy(), header)

            if new_datas_select is None:
                continue

            new_datas_select['ScriptManager1'] = 'UpdatePanel1|btn_Query'
            new_datas_select['rd_SiteType'] = '1'
            new_datas_select['__EVENTARGUMENT'] = ''

            if new_datas_select['tvsite_ExpandState'] == '':
                new_datas_select['tvsite_ExpandState'] = 'ennnnnnnnnnnnnnn'

            new_datas_click = self.get_enperprise_tvsitet(new_datas_select.copy(), header)

            if new_datas_click is None:
                continue

            last_update_time = datetime.strptime(qy_info['monitortime'], '%Y-%m-%d %H:%M:%S')
            start_date = last_update_time.strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = self.parser.set_date(start_date).set_time('00:00:00').datetime
            end_date = self.parser.set_date(end_date).set_time('00:00:00').datetime
            month = self.get_months(start_date, end_date) + 1

            for i in range(0, month):
                start_time = start_date.strftime('%Y-%m-%d')
                m = int(start_date.strftime('%m'))
                y = int(start_date.strftime('%Y'))

                if i > 0:
                    m = m + 1
                    if m > 12:
                        y = int(start_date.strftime('%Y')) + int(m / 12)
                        m = m - 12 * int(m / 12)

                    start_time = str(y) + '-' + str(m) + '-01'
                    if m < 10:
                        start_time = str(y) + '-0' + str(m) + '-01'

                if i == month - 1:
                    end_time = end_date.strftime('%Y-%m-%d')
                else:
                    mdays = calendar.monthrange(y, m)[1]
                    end_time = start_time.split('-')[0] + '-' + start_time.split('-')[1] + '-' + str(mdays)

                start_date = self.parser.set_date(start_time).set_time('00:00:00').datetime
                new_datas_click['txtStartDate_autoData'] = start_time
                new_datas_click['txtEndDate_autoData'] = end_time
                dev_datas = self.pick_dev_data(new_datas_click.copy(), header)

                if dev_datas is not None:
                    self.insert_dev_datas(dev_datas, qy_id)

                page_info = pq(dev_datas).find('div#Asp_AutoData table tr').find('td')
                pages = page_info.eq(0).find('font').eq(3).text()

                con_list = dev_datas.split('|')
                index_viewstate = con_list.index('__VIEWSTATE')
                index_eventvalidation = con_list.index('__EVENTVALIDATION')

                new_dev_data_page = new_datas_click.copy()
                new_dev_data_page['__EVENTARGUMENT'] = ''

                if pages == '' or int(pages) < 2:
                    continue

                for page in range(2, int(pages) + 1):
                    new_dev_data_page['Asp_AutoData_input'] = str(page)
                    dev_datas = self.pick_dev_data(new_dev_data_page.copy(), header)

                    if dev_datas is not None:
                        self.insert_dev_datas(dev_datas, qy_id)

    def pick_all(self):
        self.log.logger.info('开始获取河北环保数据')
        qy_infos = self.get_all_qyname_by_provinceid(self.province_id, 1)
        # print("---------------", qy_infos)
        header = {'Connection': 'keep-alive',
                  'Origin': 'http://121.28.49.84:8003',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  'Cache-Control': 'no-cache',
                  'X-Requested-With': 'XMLHttpRequest',
                  'X-MicrosoftAjax': 'Delta=true',
                  'Accept': '*/*',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                  'Referer': 'http://121.28.49.84:8003/',
                  'Accept-Encoding': 'gzip, deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9',
                  'Host': '121.28.49.84:8003',
                  # 'Upgrade-Insecure-Requests': 1,
                  }

        self.pick_data(qy_infos, header)


if __name__ == '__main__':
    t = time.time()
    he = HEEmissionPickerData()
    he.pick_all()
    print('time----------------->', time.time() - t)
