# -*- coding: utf-8 -*-

from tgspiders.lib.sch import JobScheduler


def init_jobs():
    from . import district_jobs, weather_jobs, coal_price_jobs, enterprise_jobs, environment_jobs, holiday_jobs
    js = JobScheduler()
    # js.add_started_job('获取全国城市及城市编码')
    # js.add_started_job('获取节假日信息')
    # js.add_interval_job('网络爬虫:爬取中联煤炭网数据', hours=5)
    js.add_interval_job('网络爬虫:爬取全国省份煤炭数据到数据中心', hours=4)

    # js.add_interval_job('网络爬虫:爬取全国及分省电煤价格指数', hours=2)
    js.add_interval_job('网络爬虫:爬取煤炭价格中心每日价格', hours=2)

    # js.add_interval_job('网络爬虫:爬取当前天气', hours=2)
    js.add_interval_job('网络爬虫:爬取天气信息', days=1)
    js.add_interval_job('网络爬虫:爬取小时天气信息', hours=1)

    # js.add_interval_job('企业信息：福建企业信息', hours=2)
    # js.add_interval_job('企业信息：河南企业信息', hours=2)
    # # js.add_interval_job('企业信息：河北企业信息', hours=2)
    # js.add_interval_job('企业信息：宁夏企业信息', hours=2)
    # # js.add_interval_job('企业信息：山东企业信息', hours=2)
    # js.add_interval_job('企业信息：天津企业信息', hours=2)
    # # js.add_interval_job('企业信息：广东企业信息', hours=2)

    # js.add_interval_job('环保数据：福建环保数据', hours=2)
    # js.add_interval_job('环保数据：河南环保数据', hours=2)
    # # 河北环保局网站已更换
    # # js.add_interval_job('环保数据：河北环保数据', hours=2)
    # js.add_interval_job('环保数据：宁夏环保数据', hours=2)
    # # 山东环保局网站目前打不开
    # # js.add_interval_job('环保数据：山东环保数据', hours=2)
    # js.add_interval_job('环保数据：天津环保数据', hours=2)
    # # 广东环保局无法获取数据
    # # js.add_interval_job('环保数据：广东环保数据', hours=2)
    # js.add_interval_job('环保数据：襄阳环保数据', hours=1)
    # js.add_interval_job('环保数据：西塞山环保数据', hours=1)
    # # js.add_cron_job('环保数据：襄阳环保数据', minute=53)
