# -*- coding: utf-8 -*-

from tgspiders.crawler.holiday.crawl_holiday import HolidayData
from tgspiders.lib.sch import JobScheduler as JS
from tgspiders.lib.log import Log


@JS.register('获取节假日信息')
def get_holiday_data():
    log = Log()
    log.logger.info('获取节假日信息')
    dd = HolidayData()
    dd.start()

