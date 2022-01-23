# -*- encoding= utf-8 -*-

from tgspiders.crawler.base import post_data, get_data
import json


def get_qy_id_url_lasttime(province_id, qy_style):
    params = {'provinceId': province_id, 'qyStyle': qy_style}
    url = "enterprise/listByProvinceIdAndQyStyle"
    return json.loads(get_data(url, params))


def qy_decetion(data):
    # url = 'environment/monitor/saveOrUpdate'
    url = 'environment/monitor/batch/modification'
    emmission_type_ = {'SO2折算': "1",
                       '二氧化硫': "1",
                       '二氧化硫(mg/m3)': "1",
                       '氮氧化物': "2",
                       '氮氧化物(mg/m3)': "2",
                       '氮氧化物（含二氧化氮和一氧化氮）': "2",
                       '氮氧化物折算': "2",
                       '颗粒物': "3",
                       '烟尘': "3",
                       '烟尘(mg/m3)': "3",
                       '烟尘折算': "3"}

    lit = list()
    for res in data:
        emission_type = 'null'
        if res['project_id'] in emmission_type_.keys():
            emission_type = emmission_type_[res['project_id']]
        else:
            emission_type = res['project_id']
        lit.append({
            "enterpriseId": res['enterprise_id'],
            "evaluationCriterion": res['evaluation_criterion'] if res['evaluation_criterion'] else "null",
            "monitorPoint": res["monitor_point"],
            "monitorTime": res["monitor_time"],
            "monitorValue": float(res['monitor_value']) if res['monitor_value'] else "null",
            "projectId": res['project_id'],
            "provinceId": int(res['province_id']),
            "standardLimitValue": float(res['standard_limit_value']) if res['standard_limit_value'] else "null",
            "emissionType": emission_type
        })

    post_data(url, lit)


def qy_message(res):
    citys = ['广州珠江电厂', '广东省韶关发电厂', '湛江中粤能源有限公司', '仁化县华粤煤矸石电力有限公司', '阳西海滨电力发展有限公司', '东莞市三联热电有限公司', '广东电力发展股份有限公司沙角A电厂',
             '广东广合电力有限公司沙角发电厂C厂', '中山火力发电有限公司', '广东大唐国际潮州发电有限责任公司', '广东粤电靖海发电有限公司', '广东省粤泷发电有限责任公司', '佛山市顺德五沙热电有限公司',
             '广州恒运热电（C）厂有限责任公司', '广州华润热电有限公司', '广州市旺隆热电有限公司', '广州中电荔新电力实业有限公司', '广东粤华发电有限责任公司', '广州珠江天然气发电有限公司',
             '广州瑞明电力股份有限公司', '深圳钰湖电力有限公司', '深圳市能源环保有限公司南山垃圾发电厂', '宝安区老虎坑垃圾发电厂二期', '深圳妈湾电力有限公司', '深圳市广前电力有限公司',
             '中海油深圳电力有限公司', '深圳大唐宝昌燃气发电有限公司', '深圳市能源环保有限公司宝安垃圾发电厂', '广东省粤电集团有限公司珠海发电厂', '珠海深能洪湾电力有限公司',
             '汕头经济特区万丰热电有限公司', '华能国际电力股份有限公司汕头电厂', '华能国际电力股份有限公司海门电厂', '南海长海发电有限公司', '南海发电一厂有限公司', '佛山市南海京能发电有限公司',
             '佛山恒益发电有限公司', '广东国华粤电台山发电有限公司', '湛江电力有限公司', '茂名臻能热电有限公司', '广东惠州天然气发电有限公司', '广东粤嘉电力有限公司', '广东红海湾发电有限公司',
             '华润电力（海丰）有限公司', '东莞深能源樟洋电力有限公司', '东莞中电新能源热电有限公司', '深南电（东莞）唯美电力有限公司', '东莞市挚能再生资源发电有限公司', '长青环保能源（中山）有限公司',
             '深南电（中山）电力有限公司', '中山市永安电力有限公司', '新会双水发电（Ｂ厂）有限公司', '韶关市坪石发电厂有限公司（Ｂ厂）', '国电（肇庆）热电有限公司', '广州发电厂有限公司',
             '广东珠海金湾发电有限公司', '广东惠州平海电厂有限公司', '广州恒运热电（Ｄ）厂有限责任公司', '广州珠江电力有限公司', '中山嘉明电力有限公司', '新会粤新热电联供有限公司',
             '东莞通明（众明）电力有限公司', '广东省韶关粤江发电有限责任公司', '深圳南山热电股份有限公司', '深圳能源集团股份有限公司东部电厂', '深圳粤能环保再生能源有限公司', '惠州深能源丰达电力有限公司',
             '东莞众明电力有限公司', '佛山市福能发电有限公司', '李坑生活垃圾焚烧发电二厂', '广州李坑生活垃圾焚烧发电厂一厂(广州威立雅固废能源技术有限公司)', '深圳市大贸环保投资有限公司',
             '深圳市能源环保有限公司盐田垃圾发电厂', '佛山市南海绿电再生能源有限公司', '佛山市顺德区顺能垃圾发电有限公司',
             '中海福建燃气发电有限公司', '东亚电力（厦门）有限公司', '福建晋江天然气发电有限公司', '创冠环保(福清)有限公司', '湄洲湾电厂', '华能国际电力股份有限公司福州电厂',
             '福州红庙岭垃圾焚烧发电有限公司', '福州天楹环保能源有限公司', '厦门华夏国际电力发展有限公司', '创冠环保(建阳)有限公司', '厦门市环境能源投资发展有限公司(厦门市东部垃圾焚烧发电厂)',
             '创冠环保(安溪)有限公司', '创冠环保(惠安)有限公司', '创冠环保(晋江)有限公司', '厦门同集热电有限公司', '福建省鸿山热电有限责任公司', '福建清源科技有限公司',
             '福建省石狮热电有限责任公司', '石狮市鸿峰环保生物工程有限公司', '华阳电业有限公司', '神华(福建雁石)发电有限责任公司', '厦门新阳热电有限公司', '福建华电永安发电有限公司',
             '福建大唐国际宁德发电有限责任公司', '福建晋江热电有限公司', '漳浦龙口热电厂', '国电泉州热电有限公司', '国电福州发电有限公司', '福建华电可门发电有限公司', '厦门海翼杏林热电有限公司',
             '厦门瑞新热电有限公司', '福建华电漳平火电有限公司', '莆田市圣元环保电力有限公司', '福建省龙岩新东阳环保净化有限公司', '南安市圣元环保电力有限公司']
    url = 'enterprise/saveOrUpdate'
    qy_style = 0
    if res['qy_wrylx'] == '废气' or res['qy_name'] in citys:
        qy_style = 1

    for k in res.keys():
        if not res[k] or res[k] == '':
            res[k] = 'null'
        res[k] = str(res[k])

    lit = [
        {
            "provinceId": int(res['province_id']),
            "qyId": res["qy_id"],
            "qyName": res["qy_name"],
            "qyWrylx": res["qy_wrylx"],
            "qyJd": res["qy_jd"],
            "qyWd": res["qy_wd"],
            "qyAddress": res["qy_address"],
            "qyCorporation": res["qy_corporation"],
            "qyIndustry": res["qy_industry"],
            "qyLinkUser": res["qy_link_user"],
            "qyLinkPhone": res["qy_link_phone"],
            "qyTysj": res["qy_tysj"],
            "qyAutoMonitorStyle": res["qy_auto_monitor_style"],
            "qyManualMonitorStyle": res["qy_manual_monitor_style"],
            "qyAutoMonitorOperationStyle": res["qy_auto_monitor_operation_style"],
            "qyPfwrwmc": res["qy_pfwrwmc"],
            "qyZyscgy": res["qy_zyscgy"],
            "qyZycp": res["qy_zycp"],
            "qyZlss": res["qy_zlss"],
            "qyLeadTime": res["qy_lead_time"],
            "qyUrl": res["qy_url"],
            "qyIntroduce": res["qy_introduce"],
            "qyOrganizationCode": res["qy_organization_code"],
            "qyLinkEmail": res["qy_link_email"],
            "qyStyle": qy_style,
            "qyUnitCategory": res["qy_unit_category"],
            "qyRegisterType": res["qy_register_type"],
            "qyManagerDept": res["qy_manager_dept"],
            "qyScale": res["qy_scale"],
            "qyFax": res["qy_fax"],
            "qyCity": res["qy_city"],
            "qyCityId": res["qy_city_id"]}
    ]

    post_data(url, lit)


if __name__ == '__main__':
    qy_message(res='')
    # get_qy_id_url_lasttime(41000000,1)
    # dic ={ 'emissionType':'3','evaluationCriterion': 'null', 'monitorTime': '2019-08-25 23:00:00', 'projectId': '烟尘', 'provinceId': 41000000, 'standardLimitValue': 30.0, 'monitorPoint': '1#锅炉脱硫岛出口', 'enterpriseId': '41170067169143-9', 'monitorValue': 1.13}
    # qy_decetion(dic)
