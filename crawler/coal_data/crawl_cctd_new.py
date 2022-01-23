# -*- coding: utf-8 -*-

import json
import requests
import datetime
from urllib.parse import urlencode
from tgspiders.lib.err_util import retry
from tgspiders.lib.http_util import HttpUtil
from tgspiders.lib.log import Log

requests.packages.urllib3.disable_warnings()


class CrawlCctd():
    def __init__(self):
        self.log = Log().logger
        self.local = HttpUtil('http://116.63.81.47:8001/load-data-write/coal/price/%s/update-batch', 'admin', 'www.togeek.cn')
        self.city = {
            "山西省": ["太原市", "古交市", "大同市", "大同矿区", "大同南郊", "左云县", "浑源县",
                    "新荣区", "阳泉市", "盂县", "平定县", "长治市", "长治郊区", "长治县", "长子县",
                    "高平市", "壶关县", "潞城市", "沁源县", "屯留县", "襄垣县", "晋城市", "泽州县",
                    "沁水县", "陵川县", "阳城县", "朔州市", "怀仁县", "山阴县", "右玉县", "平鲁区",
                    "平遥县", "榆次区", "左权县", "介休市", "和顺县", "灵石县", "寿阳县", "河津市",
                    "平陆县", "忻州市", "宁武县", "静乐县", "河曲县", "原平市", "保德县", "临汾市",
                    "乡宁县", "翼城县", "蒲县", "汾西县", "古县", "洪洞县", "侯马市", "霍州市",
                    "柳林县", "孝义市", "兴县", "离石区", "山西省"],
            "内蒙古": ["包头市", "乌海市", "赤峰市", "霍林郭勒市", "鄂尔多斯市", "东胜区", "达拉特旗",
                    "准格尔旗", "伊金霍洛旗", "海拉尔区"],
            "陕西省": ["陕北区", "铜川市", "宝鸡市", "彬县", "旬邑县", "彬长地区", "神木县",
                    "府谷县", "榆阳区", "子长县", "黄陵县", "韩城市", "澄城县", "陕西省"],
            "河南省": ["郑州市", "安阳市", "鹤壁市", "平顶山市", "焦作市", "永城市", "三门峡市",
                    "义马市", "许昌市", "禹州市"],
            "贵州省": ["贵阳市", "安顺市", "遵义市", "黔西南", "毕节市", "纳雍县", "金沙县",
                    "织金县", "六盘水市"],
            "山东省": ["临沂市", "泰安市", "淄博市", "济宁市", "兖州市", "枣庄市", "滕州市", "山东省"],
            "安徽省": ["淮北市", "淮南市", "宿州市", "安徽省"],
            "甘肃省": ["武威市", "兰州市", "华亭县", "靖远县"],
            "河北省": ["邯郸市", "石家庄市", "唐山市", "邢台市", "张家口市", "河北省"],
            "黑龙江": ["鹤岗市", "鸡西市", "七台河市", "双鸭山市"],
            "湖南省": ["郴州市", "涟源市", "娄底市", "湘潭市", "株洲市"],
            "吉林省": ["通化市"],
            "江苏省": ["徐州市"],
            "江西省": ["萍乡市"],
            "辽宁省": ["本溪市", "丹东市", "抚顺市", "阜新市"],
            "宁夏区": ["石嘴山市", "大武口区", "灵武市"],
            "青海省": ["西宁市", "天峻县"],
            "四川省": ["达州市", "攀枝花市", "宜宾市"],
            "新疆区": ["乌鲁木齐市", "阜康县", "哈密市"],
            "云南省": ["昆明市", "昭通市", "富源县", "宣威市"],
            "浙江省": ["杭州市", "金华市", "宁波市", "衢州市", "绍兴市", "台州市", "温州市", "乍浦镇"],
            "重庆市": ["永川区", "云阳县", "巫山县", "重庆市"]
        }

    @retry
    def crawl_data(self, city, start_date, end_date, name):
        params = {
            "data": city,
            "name": name,
            # "time": " where  DATE_FORMAT(END_DATE,'%Y-%m-%d') >= '-0006-11-30'",   # 获取全部数据
            "time": "where  DATE_FORMAT(END_DATE,'%Y-%m-%d') BETWEEN '" + start_date + "' and '" + end_date + "'",
            "draw": "1",
            "columns[0][data]": "0",
            "columns[0][name]": "",
            "columns[0][searchable]": "true",
            "columns[0][orderable]": "false",
            "columns[0][search][value]": "",
            "columns[0][search][regex]": "false",
            "columns[1][data]": "1",
            "columns[1][name]": "",
            "columns[1][searchable]": "true",
            "columns[1][orderable]": "false",
            "columns[1][search][value]": "",
            "columns[1][search][regex]": "false",
            "columns[2][data]": "2",
            "columns[2][name]": "",
            "columns[2][searchable]": "true",
            "columns[2][orderable]": "false",
            "columns[2][search][value]": "",
            "columns[2][search][regex]": "false",
            "columns[3][data]": "3",
            "columns[3][name]": "",
            "columns[3][searchable]": "true",
            "columns[3][orderable]": "false",
            "columns[3][search][value]": "",
            "columns[3][search][regex]": "false",
            "columns[4][data]": "4",
            "columns[4][name]": "",
            "columns[4][searchable]": "true",
            "columns[4][orderable]": "false",
            "columns[4][search][value]": "",
            "columns[4][search][regex]": "false",
            "columns[5][data]": "5",
            "columns[5][name]": "",
            "columns[5][searchable]": "true",
            "columns[5][orderable]": "false",
            "columns[5][search][value]": "",
            "columns[5][search][regex]": "false",
            "columns[6][data]": "6",
            "columns[6][name]": "",
            "columns[6][searchable]": "true",
            "columns[6][orderable]": "false",
            "columns[6][search][value]": "",
            "columns[6][search][regex]": "false",
            "columns[7][data]": "7",
            "columns[7][name]": "",
            "columns[7][searchable]": "true",
            "columns[7][orderable]": "false",
            "columns[7][search][value]": "",
            "columns[7][search][regex]": "false",
            "columns[8][data]": "8",
            "columns[8][name]": "",
            "columns[8][searchable]": "true",
            "columns[8][orderable]": "false",
            "columns[8][search][value]": "",
            "columns[8][search][regex]": "f"
        }
        url = 'https://www.cctd.com.cn/datasql.php'
        headers = {
            'Host': 'www.cctd.com.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cookie': 'acw_tc=2760825415953348244997697e4cfdb3a8ce26588631c796bec5a568daf861',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
        r = requests.get(url, params=urlencode(params, encoding='gbk'), headers=headers, timeout=120,
                         verify=False)
        return r.text.encode(r.encoding).decode('utf-8') if r.ok else None

    def crawl_dqjg(self, start_date, end_date):
        '''一天一次'''
        for key, value in self.city.items():
            for city in value:
                data = self.crawl_data(city, start_date, end_date, '煤炭价格')
                if data:
                    self.parse_area_coal_text(city, json.loads(data))

    def parse_area_coal_text(self, city, data):
        res = {'plant_app_etl.tb_etl_area_coal_price': [['date', 'area', 'name', 'ash', 'volatile', 'sulfur',
                                                         'bond', 'thermal', 'price', 'price_type']]}
        result = list()
        if isinstance(data, dict) and 'data' in data:
            for x in data['data']:
                if len(set(x)) < 2:
                    continue
                con = dict()
                con['date'] = x[0]
                con['area'] = x[1]
                con['name'] = x[2]
                con['ash'] = x[3]
                con['volatile'] = x[4]
                con['sulfur'] = x[5]
                con['bond'] = x[6]
                con['thermal'] = x[7]
                con['price'] = x[8]
                con['price_type'] = x[9]
                result.append(con)

            res['plant_app_etl.tb_etl_area_coal_price'].append(result)
            r = self.local.post(['data', 'receive', 'oms', 'data'], data=res, timeout=60)
            self.log.info('post %s 数据========>>>> %s' % (city, r))

    def crawl_zdmkkc(self, start_date, end_date):
        '''十天一次'''
        res = {'plant_app_etl.tb_etl_emphasis_coal': [['date', 'area', 'value', 'link_ratio', 'same_ratio']]}
        result = list()
        data = self.crawl_data('重点煤矿库存', start_date, end_date, '重点煤矿库存')
        data = json.loads(data)

        if isinstance(data, dict) and 'data' in data:
            for x in data['data']:
                if len(set(x)) < 2:
                    continue
                con = dict()
                con['date'] = x[0]
                con['area'] = x[1]
                con['value'] = x[2]
                con['link_ratio'] = x[3]
                con['same_ratio'] = x[4]
                result.append(con)
            res['plant_app_etl.tb_etl_emphasis_coal'].append(result)
            r = self.local.post(['data', 'receive', 'oms', 'data'], data=res, timeout=60)
            self.log.info('post 重点煤矿库存 数据========>>>> %s  %s' % r)

    def crawl_yhlddc(self, start_date, end_date):
        '''一天一次'''
        res = {'plant_app_etl.tb_etl_six_powerplant': [['date', 'name', 'consumption', 'inventory', 'days']]}
        result = list()
        data = self.crawl_data('沿海六大电厂(日)', start_date, end_date, '沿海六大电厂(日)')
        data = json.loads(data)
        if isinstance(data, dict) and 'data' in data:
            for x in data['data']:
                if len(set(x)) < 2:
                    continue
                con = dict()
                con['date'] = x[0]
                con['name'] = x[1]
                con['consumption'] = x[2]
                con['inventory'] = x[3]
                con['days'] = x[4]
                result.append(con)
            res['plant_app_etl.tb_etl_six_powerplant'].append(result)
            r = self.local.post(['data', 'receive', 'oms', 'data'], data=res, timeout=60)
            self.log.info('post 沿海六大电厂(日) 数据========>>>> %s  %s' % r)

    def crawl_qgzddc(self, start_date, end_date):
        res = {'plant_app_etl.tb_etl_emphasis_powerplant': [["date", "power_grid", "supply", "consume",
                                                             "inventory", "days"]]}
        result = list()
        data = self.crawl_data('全国重点电厂', start_date, end_date, '全国重点电厂')
        data = json.loads(data)
        if isinstance(data, dict) and 'data' in data:
            for x in data['data']:
                if len(set(x)) < 2:
                    continue
                con = dict()
                con['date'] = x[0]
                con['power_grid'] = x[1]
                con['supply'] = x[2]
                con['consume'] = x[3]
                con['inventory'] = x[4]
                con['days'] = x[5]
                result.append(con)
            res['plant_app_etl.tb_etl_emphasis_powerplant'].append(result)
            r = self.local.post(['data', 'receive', 'oms', 'data'], data=res, timeout=60)
            self.log.info('post 全国重点电厂 数据========>>>> %s  %s' % r)

    def crawl_zgdmjgzs(self, start_date, end_date):
        res = {'plant_app_etl.tb_etl_electric_coal': [["date", "area", "price", "same_ratio", "link_ratio"]]}
        result = list()
        data = self.crawl_data('中国电煤价格指数', start_date, end_date, '中国电煤价格指数')
        data = json.loads(data)
        if isinstance(data, dict) and 'data' in data:
            for x in data['data']:
                if len(set(x)) < 2:
                    continue
                con = dict()
                con['date'] = x[0] + '-01'
                con['area'] = x[1]
                con['price'] = x[2]
                con['link_ratio'] = x[3]
                con['same_ratio'] = x[4]
                result.append(con)
            res['plant_app_etl.tb_etl_electric_coal'].append(result)
            r = self.local.post(['data', 'receive', 'oms', 'data'], data=res, timeout=60)
            self.log.info('post 中国电煤价格指数 数据========>>>> %s  %s' % r)

    def get_his_data(self, start_date, end_date):
        try:
            self.crawl_dqjg(start_date, end_date)
        except Exception as e:
            self.log.error(e)

        self.crawl_zdmkkc(start_date, end_date)
        self.crawl_yhlddc(start_date, end_date)
        self.crawl_qgzddc(start_date, end_date)
        self.crawl_zgdmjgzs(start_date, end_date)

    def start(self):
        today = datetime.datetime.now()
        begin = (today - datetime.timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        today = today.strftime('%Y-%m-%d %H:%M:%S')

        try:
            self.crawl_dqjg(begin, today)
            self.crawl_zdmkkc(begin, today)
            self.crawl_yhlddc(begin, today)
            self.crawl_qgzddc(begin, today)
            self.crawl_zgdmjgzs(begin, today)
        except Exception as e:
            self.log.error(e)


if __name__ == '__main__':
    gcodc = CrawlCctd()
    gcodc.start()
