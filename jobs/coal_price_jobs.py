# -*- coding: utf-8 -*-

from tgspiders.crawler.coal_data.crawl_electric_coal_price import CrawlElectricCoalPrice
from tgspiders.crawler.coal_data.crawl_coal_price import CrawlCoalPrice
from tgspiders.crawler.coal_data.crawl_cctd import CrawlCctd
from tgspiders.crawler.coal_data.data_center_province_coal import DataCenterProvinceCoal
from tgspiders.lib.sch import JobScheduler as JS
from tgspiders.lib.log import Log

log = Log()


@JS.register('网络爬虫:爬取中联煤炭网数据')
def pick_cctd():
    log.logger.info('爬取爬取中联煤炭网数据')
    cctd = CrawlCctd()
    cctd.start()


@JS.register('网络爬虫:爬取全国省份煤炭数据到数据中心')
def data_center_province_coal():
    log.logger.info('爬取全国各个省份煤炭信息，转储到数据中心')
    coal_network = DataCenterProvinceCoal()
    coal_network.start()


@JS.register('网络爬虫:爬取全国及分省电煤价格指数')
def pick_electric_coal_price():
    log.logger.info('爬取全国及分省电煤价格指数')
    ccd = CrawlElectricCoalPrice()
    ccd.start()


@JS.register('网络爬虫:爬取煤炭价格中心每日价格')
def crawl_coal_price_data():
    log.logger.info('爬取煤炭价格中心每日价格')
    ccp = CrawlCoalPrice()
    ccp.start()
    ccp.get_his_data(100)
