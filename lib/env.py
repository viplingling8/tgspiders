# -*- coding: utf-8 -*-

from tglibs.config import ConfigBase, ConfigProperty
from tglibs.singleton import Singleton
import os


class Config(ConfigBase, metaclass=Singleton):
    db_base_url = ConfigProperty(str)
    db = ConfigProperty(str)
    db_host = ConfigProperty(str)
    db_port = ConfigProperty(int)
    db_user = ConfigProperty(str)
    db_passwd = ConfigProperty(str)
    error_count = ConfigProperty(int, default=5)
    http_timeout = ConfigProperty(int)

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_filename = os.path.join(base_dir, 'tgspiders.ini')
        super(Config, self).__init__(config_filename)
        self.load()

Environment = Config