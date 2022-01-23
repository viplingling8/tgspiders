# -*- coding: utf-8 -*-

import requests
import json
from tgspiders.lib.err_util import retry
from tgspiders.lib.log import Log

# host = '39.98.43.197'
# host = '116.63.81.47'
host = '101.43.124.209'
port = 8000
# host = '127.0.0.1'
# port = 80

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML,"
                  " like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Content-Type": "application/json",
    "Connection": "keep-alive"
}


@retry
def post_data(url, data):
    base_url = 'http://%s:%s/load-data-write/' % (host, port)
    # headers["Referer"] = "%sswagger-ui.html" % (base_url)
    headers["Origin"] = "http://%s:%s" % (host, port)
    headers["Host"] = "%s:%s" % (host, port)

    try:
        r = requests.post(base_url + url + '?key=Songan123', headers=headers, data=json.dumps(data))
        return r.ok
    except Exception as e:
        Log().logger.info(e)
        return False


def get_data(url, params=None):
    base_url = 'http://%s:%s/load-data/' % (host, port)
    headers["Referer"] = "%sswagger-ui.html" % (base_url)
    headers["Origin"] = "http://%s:%s" % (host, port)
    headers["Host"] = "%s:%s" % (host, port)

    try:
        r = requests.get(base_url + url + '?key=togeek', headers=headers, params=params)
        return r.text if r.ok else None

    except Exception as e:
        Log().logger.info(e)
        return False


if __name__ == "__main__":
    res = post_data('crawler/coalprice/fygjg', data={'key1':'value1','key2':'value2'})
    print(res)

