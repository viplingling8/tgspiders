# -*- coding: utf-8 -*-

from tgspiders.lib.http_util import HttpUtil
import abc

class Base(metaclass=abc.ABCMeta):
    def __init__(self, base_url):
        self.http = HttpUtil(base_url)

        self.qy_style = ['qy_id', 'qy_name', 'qy_wrylx', 'qy_jd', 'qy_wd', 
            'qy_address', 'qy_corporation', 'qy_industry', 'qy_link_user', 
            'qy_link_phone', 'qy_tysj', 'qy_auto_monitor_style', 
            'qy_manual_monitor_style', 'qy_auto_monitor_operation_style', 
            'qy_pfwrwmc', 'qy_zyscgy', 'qy_zycp', 'qy_zlss', 'qy_lead_time', 
            'qy_url', 'qy_introduce', 'qy_organization_code', 'province_id', 
            'qy_link_email', 'qy_unit_category', 'qy_register_type', 
            'qy_manager_dept', 'qy_scale', 'qy_fax', 'qy_city', 'qy_city_id'
        ]

    def insert_enterprise_info(self, data):
        pass
        # if data:
        #     insert_sql = '''INSERT `environmental_data`.`tb_enterprise` (
        #         qy_id, qy_name, qy_wrylx, qy_jd, qy_wd, qy_address,
        #         qy_corporation, qy_industry, qy_link_user, qy_link_phone,
        #         qy_tysj, qy_auto_monitor_style, qy_manual_monitor_style,
        #         qy_auto_monitor_operation_style, qy_pfwrwmc, qy_zyscgy,
        #         qy_zycp, qy_zlss, qy_lead_time, qy_url, qy_introduce,
        #         qy_organization_code, province_id, qy_link_email,
        #         qy_unit_category, qy_register_type, qy_manager_dept,
        #         qy_scale, qy_fax, qy_city, qy_city_id) VALUES (%(qy_id)s,
        #         %(qy_name)s, %(qy_wrylx)s, %(qy_jd)s, %(qy_wd)s, %(qy_address)s,
        #         %(qy_corporation)s, %(qy_industry)s, %(qy_link_user)s,
        #         %(qy_link_phone)s, %(qy_tysj)s, %(qy_auto_monitor_style)s,
        #         %(qy_manual_monitor_style)s, %(qy_auto_monitor_operation_style)s,
        #         %(qy_pfwrwmc)s, %(qy_zyscgy)s, %(qy_zycp)s, %(qy_zlss)s,
        #         %(qy_lead_time)s, %(qy_url)s, %(qy_introduce)s,
        #         %(qy_organization_code)s, %(province_id)s, %(qy_link_email)s,
        #         %(qy_unit_category)s, %(qy_register_type)s, %(qy_manager_dept)s,
        #         %(qy_scale)s, %(qy_fax)s, %(qy_city)s, %(qy_city_id)s);'''
        #     update_sql = '''UPDATE `environmental_data`.`tb_enterprise` SET
        #         `qy_name`=%(qy_name)s, `qy_wrylx`=%(qy_wrylx)s,
        #         `qy_jd`=%(qy_jd)s,
        #         `qy_wd`=%(qy_wd)s, `qy_address`=%(qy_address)s,
        #         `qy_corporation`=%(qy_corporation)s,
        #         `qy_industry`=%(qy_industry)s,
        #         `qy_link_user`=%(qy_link_user)s,
        #         `qy_link_phone`=%(qy_link_phone)s,
        #         `qy_tysj`=%(qy_tysj)s,
        #         `qy_auto_monitor_style`=%(qy_auto_monitor_style)s,
        #         `qy_manual_monitor_style`=%(qy_manual_monitor_style)s,
        #         `qy_auto_monitor_operation_style`=%(qy_auto_monitor_operation_style)s,
        #         `qy_pfwrwmc`=%(qy_pfwrwmc)s, `qy_zyscgy`=%(qy_zyscgy)s,
        #         `qy_zycp`=%(qy_zycp)s, `qy_zlss`=%(qy_zlss)s,
        #         `qy_lead_time`=%(qy_lead_time)s, `qy_url`=%(qy_url)s,
        #         `qy_introduce`=%(qy_introduce)s,
        #         `qy_organization_code`=%(qy_organization_code)s ,
        #         `qy_link_email`=%(qy_link_email)s,
        #         `qy_unit_category`=%(qy_unit_category)s,
        #         `qy_register_type`=%(qy_register_type)s,
        #         `qy_manager_dept`=%(qy_manager_dept)s,
        #         `qy_scale`=%(qy_scale)s, `qy_fax`=%(qy_fax)s,
        #         `qy_city`=%(qy_city)s,
        #         `qy_city_id`=%(qy_city_id)s WHERE (`qy_id`=%(qy_id)s) AND (
        #             `province_id`=%(province_id)s) ;'''
        #     self.insert_update(insert_sql, update_sql, data)

    def insert_update(self, insert_sql, update_sql, con):
        pass