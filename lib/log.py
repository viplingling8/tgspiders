# -*- coding: utf-8 -*-

from tglibs.log import Log, get_log_config
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_filename = os.path.join(base_dir, 'tgspiders.ini')
log_config = get_log_config(config_filename, 'LOG')
log_config.load()
Log.from_config(log_config)