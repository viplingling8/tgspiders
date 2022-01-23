# -*- coding: utf-8 -*-

from tgspiders.lib.env import Environment
from tgspiders.lib.log import Log
import traceback
import time


def retry(func):
    def _inner(*args, **kwargs):
        env = Environment()
        logger = Log().logger
        for i in range(env.error_count):
            try:
                logger.info('execute: %s' % func.__name__)
                return func(*args, **kwargs)
            except:
                l = ['retry(%s): %s' % (i + 1, func.__name__), traceback.format_exc()]
                logger.error('\n'.join(l))
                time.sleep(0.5)

    _inner.__name__ = func.__name__
    return _inner
