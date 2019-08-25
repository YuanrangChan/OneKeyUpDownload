__author__ = 'laiyu'

import configparser
from otherTools import OtherTools

class HostConfigParser:
    def __init__(self):
        self.config = configparser.ConfigParser()
        encoding = OtherTools().get_file_encoding('./conf/host_config.conf')
        self.config.read('./conf/host_config.conf', encoding='utf-8')

    def get_host_config(self):
        return self.config

#20190825 No changes.
