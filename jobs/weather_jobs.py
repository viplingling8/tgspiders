# -*- coding: utf-8 -*-

from tgspiders.crawler.weather.pick_realtime_weather import PickRealtimeWeather
from tgspiders.crawler.weather.pick_weather import PickWeather
from tgspiders.crawler.weather.pick_hour_weather import PickHourWeather
from tgspiders.lib.sch import JobScheduler as JS
from tgspiders.lib.log import Log

log = Log()


@JS.register('网络爬虫:爬取当前天气')
def pick_realtime_weather():
    log.logger.info('爬取当前天气')
    prw = PickRealtimeWeather()
    prw.crawl()


@JS.register('网络爬虫:爬取天气信息')
def pick_weather():
    log.logger.info('爬取天气信息')
    pw = PickWeather()
    pw.start()


@JS.register('网络爬虫:爬取小时天气信息')
def pick_hour_weather():
    log.logger.info('爬取小时天气信息')
    pw = PickHourWeather()
    pw.crawl()
