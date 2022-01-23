# -*- coding: utf-8 -*-

from tgspiders.crawler.environmental_data.crawler_all_enterprise.pick_tj_enterprise_all import TJEmissionPicker
from tgspiders.crawler.environmental_data.crawler_all_enterprise.pick_fj_enterprise_all import FJEmissionPicker
from tgspiders.crawler.environmental_data.crawler_all_enterprise.pick_ha_enterprise_all import HAEmissionPicker
from tgspiders.crawler.environmental_data.crawler_all_enterprise.pick_he_enterprise_all import HEEmissionPicker
from tgspiders.crawler.environmental_data.crawler_all_enterprise.pick_nx_enterprise_all import NXEmissionPicker
from tgspiders.crawler.environmental_data.crawler_all_enterprise.pick_sd_enterprise_all import SDEmissionPicker
from tgspiders.crawler.environmental_data.crawler_all_enterprise.pick_gd_enterprise_all import GDEmissionPicker
from tgspiders.lib.sch import JobScheduler as JS
from tgspiders.lib.log import Log

@JS.register('企业信息：福建企业信息')
def ln_environment_data():
    log = Log()
    log.logger.info('福建企业信息')
    ln = FJEmissionPicker()
    ln.pick_all()

@JS.register('企业信息：河南企业信息')
def ln_environment_data():
    log = Log()
    log.logger.info('河南企业信息')
    ln = HAEmissionPicker()
    ln.pick_all()

@JS.register('企业信息：河北企业信息')
def ln_environment_data():
    log = Log()
    log.logger.info('河北企业信息')
    ln = HEEmissionPicker()
    ln.pick_all()

@JS.register('企业信息：宁夏企业信息')
def ln_environment_data():
    log = Log()
    log.logger.info('宁夏企业信息')
    ln = NXEmissionPicker()
    ln.pick_all()

@JS.register('企业信息：山东企业信息')
def ln_environment_data():
    log = Log()
    log.logger.info('山东企业信息')
    ln = SDEmissionPicker()
    ln.pick_all()

@JS.register('企业信息：天津企业信息')
def ln_environment_data():
    log = Log()
    log.logger.info('天津企业信息')
    ln = TJEmissionPicker()
    ln.pick_all()

@JS.register('企业信息：广东企业信息')
def ln_environment_data():
    log = Log()
    log.logger.info('广东企业信息')
    ln = GDEmissionPicker()
    ln.pick_all()