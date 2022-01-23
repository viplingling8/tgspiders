# -*- coding: utf-8 -*-

from tgspiders.crawler.environmental_data.crawler_enterprise_environmental_data import *
from tgspiders.lib.sch import JobScheduler as JS
from tgspiders.lib.log import Log


@JS.register('环保数据：福建环保数据')
def fj_environment_data():
    log = Log()
    log.logger.info('福建环保数据')
    ln = FJEmissionPickerData()
    ln.pick_all()


@JS.register('环保数据：襄阳环保数据')
def xy_environment_data():
    log = Log()
    log.logger.info('襄阳环保数据')
    ln = CrawlerHbXYAllData()
    ln.pick_all()


@JS.register('环保数据：西塞山环保数据')
def xss_environment_data():
    log = Log()
    log.logger.info('西塞山环保数据')
    ln = XSSmissionPickerData()
    ln.pick_all()


@JS.register('环保数据：河南环保数据')
def ha_environment_data():
    log = Log()
    log.logger.info('河南环保数据')
    ln = HAEmissionPickerData()
    ln.pick_all()


@JS.register('环保数据：河北环保数据')
def he_environment_data():
    log = Log()
    log.logger.info('河北环保数据')
    ln = HEEmissionPickerData()
    ln.pick_all()


@JS.register('环保数据：宁夏环保数据')
def nx_environment_data():
    log = Log()
    log.logger.info('宁夏环保数据')
    ln = NXEmissionPickerData()
    ln.pick_all()


@JS.register('环保数据：山东环保数据')
def sd_environment_data():
    log = Log()
    log.logger.info('山东环保数据')
    ln = SDEmissionPickerData()
    ln.pick_all()


@JS.register('环保数据：天津环保数据')
def tj_environment_data():
    log = Log()
    log.logger.info('天津环保数据')
    ln = TJEmissionPickerData()
    ln.pick_all()


@JS.register('环保数据：广东环保数据')
def gd_environment_data():
    log = Log()
    log.logger.info('广东环保数据')
    ln = CrawlGdEnvData()
    ln.crawl()
