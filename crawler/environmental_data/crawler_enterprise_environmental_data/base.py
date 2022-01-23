# -*- coding: utf-8 -*-

from tglibs.date_time_parser import DateTimeParser
from tgspiders.lib.http_util import HttpUtil
from datetime import datetime
import abc
from tgspiders.lib.post_root import get_qy_id_url_lasttime


class Base(metaclass=abc.ABCMeta):
    def __init__(self, base_url):
        self.http = HttpUtil(base_url)
        self.parser = DateTimeParser()
        self.sql_type = ['province_id', 'enterprise_id', 'monitor_point',
                         'monitor_time', 'project_id', 'monitor_value',
                         'standard_limit_value', 'evaluation_criterion']
        self.parseProvinces = [65000000]

    def get_point_last_update_time(self, province_id, enterprise_id, dev_name, default_date='2017-01-01'):
        last_update_time = None
        qyid = "'%s'" % enterprise_id
        monitor_point = "'%s'" % dev_name
        return last_update_time if last_update_time else \
            DateTimeParser().set_date(default_date).set_time(
                '00:00:00').datetime

    def get_all_qyid_by_province_id(self, province_id):
        list_qyid = None
        return list_qyid

    def get_all_qyid_by_qy_wrylx(self, province_id, qy_style):
        list_qyinfo = []
        list_qy = get_qy_id_url_lasttime(province_id, qy_style)

        for k in list_qy:
            dev = dict()
            dev['qy_id'] = k['qyid']
            dev['qy_url'] = k['qyurl']
            dev['monitortime'] = k['monitortime'] if k['monitortime'] else '2019-01-01 00:00:00'
            list_qyinfo.append(dev)
        return list_qyinfo

    def get_province_data(self, province_id, begin_time, end_time=datetime.now()):
        list_datas = []
        return list_datas

    def get_last_update_time(self, province_id, enterprise_id, default_date='2016-12-01'):
        last_update_time = None
        qyid = "'%s'" % enterprise_id

        return last_update_time if last_update_time else \
            DateTimeParser().set_date(default_date).set_time(
                '00:00:00').datetime
