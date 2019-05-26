#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
import hashlib
from conf import settings


class Encryption(object):
    """加密相关"""
    def __init__(self):
        self.coding = "utf8"

    def md5_encry(self, str_p):
        """密码进行md5加密"""
        md5 = hashlib.md5(settings.md5_salt.encode(self.coding))
        md5.update(str_p.encode(self.coding))
        return md5.hexdigest()



