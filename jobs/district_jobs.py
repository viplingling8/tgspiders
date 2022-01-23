# -*- coding: utf-8 -*-

from tgspiders.crawler.district_data.crawl_district import DistrictData
from tgspiders.lib.sch import JobScheduler as JS
from tgspiders.lib.log import Log


@JS.register('获取全国城市及城市编码')
def get_city_citycode():
    log = Log()
    log.logger.info('获取全国城市及城市编码')
    dd = DistrictData()
    dd.start()

