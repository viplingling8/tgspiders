# -*- coding: utf-8 -*-

from urllib.parse import urljoin, urlencode
from requests.auth import HTTPBasicAuth
from tgspiders.lib.log import Log
from tglibs.easy_json import o2j
import traceback
import requests


class HttpUtil:
    def __init__(self, base_url, user_name=None, password=None):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(user_name, password) if all([user_name, password]) else None
        self.session = requests.Session()
        self.log = Log()

    def join_url(self, path):
        return urljoin(self.base_url, '/'.join(map(str, path)))

    @staticmethod
    def handle(response, handler):
        if not response:
            return None, False
        handler = handler or 'raw'
        if handler not in ['text', 'json', 'content', 'raw']:
            raise Exception('无法识别的处理无法')
        return ((response.json() if handler == 'json' else
                 (response.text if handler == 'text' else
                  (response.content if handler == 'content' else
                   response))),
                response.ok)

    def get(self, path, params=None, timeout=None, handler='json', headers=None):
        try:
            timeout = timeout or 5
            r = self.session.get(self.join_url(path), params=params, auth=self.auth, timeout=timeout, headers=headers)
            return self.handle(r, handler)
        except:
            self.log.logger.info('HTTP GET Error:%s\n' % traceback.format_exc())
            return None, False

    def put(self, path, params=None, data=None, timeout=None, handler='json'):
        try:
            timeout = timeout or 5
            h = {'Content-Type': 'application/json'}
            r = self.session.put(self.join_url(path), headers=h, params=params,
                                 data=o2j(data, True) if data is not None else data,
                                 auth=self.auth, timeout=timeout)
            return self.handle(r, handler)
        except:
            self.log.logger.info('HTTP PUT Error:%s\n' % traceback.format_exc())
            return None, False

    def post(self, path, params=None, data=None, timeout=None, handler='json', headers=None):
        try:
            timeout = timeout or 5
            if handler == 'json':
                headers = {'Content-Type': 'application/json'}
            r = self.session.post(self.join_url(path), headers=headers, params=params,
                                  data=o2j(data, True) if data is not None else data,
                                  auth=self.auth, timeout=timeout)
            return self.handle(r, handler)
        except:
            self.log.logger.info('HTTP POST Error:%s\n' % traceback.format_exc())
            return None, False

    def delete(self, path, params=None, timeout=None, handler='json'):
        try:
            timeout = timeout or 5
            r = self.session.delete(self.join_url(path), params=params, auth=self.auth, timeout=timeout)
            return self.handle(r, handler)
        except:
            self.log.logger.info('HTTP DELETE Error:%s\n' % traceback.format_exc())
            return None, False

    @staticmethod
    def generate_trans_params(plants, uri, proxy, params):
        plants = [plants] if isinstance(plants, (int, str)) else list(plants)
        result = {'plants': ','.join(map(str, plants))}
        if proxy:
            result['proxy'] = 'true'
        uri = list(uri) if isinstance(uri, (list, tuple)) else [uri]
        result['uri'] = '/%s' % '/'.join(map(str, uri))
        if params:
            result['uri'] += '?%s' % urlencode(params)
        return result

    def trans_get(self, plants, uri, proxy=False, params=None, timeout=None, handler='json'):
        params = self.generate_trans_params(plants, uri, proxy, params)
        return self.get(['distribute', 'trans'], params=params, timeout=timeout, handler=handler)

    def trans_post(self, plants, uri, proxy=False, params=None, data=None, timeout=None, handler='json'):
        params = self.generate_trans_params(plants, uri, proxy, params)
        return self.post(['distribute', 'trans'], params=params, data=data, timeout=timeout, handler=handler)

    def trans_put(self, plants, uri, proxy=False, params=None, data=None, timeout=None, handler='json'):
        params = self.generate_trans_params(plants, uri, proxy, params)
        return self.put(['distribute', 'trans'], params=params, data=data, timeout=timeout, handler=handler)

    def trans_delete(self, plants, uri, proxy=False, params=None, timeout=None, handler='json'):
        params = self.generate_trans_params(plants, uri, proxy, params)
        return self.delete(['distribute', 'trans'], params=params, timeout=timeout, handler=handler)
