#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
"""服务端主要功能集合"""
import os
from core.handle_db import HandleDb
from conf import settings
from core.transfer_dict import TransferDic
from core.encryption import Encryption


class Action(object):

    def __init__(self):
        self.ep = Encryption()  # 实例化加密

    def send_accept_server(self, dic):
        """发送消息给服务端并接受返回数据"""
        td = TransferDic(self.client)
        td.send_packget_dict(dic)
        recv_dic = td.accept_packget_dict()
        return recv_dic

    def login(self, socket, user_info):
        """登录相关"""
        username = user_info['username']
        password = user_info['password']
        # 读取userinfo文件,查看用户和密码是否正确
        td = TransferDic(socket)
        for user in HandleDb.read_file(settings.user_path):
            userinfo_list = user.split("|")
            user = userinfo_list[0].strip()
            passwd = userinfo_list[1].strip()
            disk_quota = userinfo_list[2].strip()
            passwd_md5 = self.ep.md5_encry(password)
            if username == user and passwd_md5 == passwd:
                # 如果已经登录成功就返回code
                td.send_packget_dict({"user_code": "3003"})
                return (username ,disk_quota)
        else:
            td.send_packget_dict({"user_code": "3004"})
            return

    def register(self, socket, user_info):
        """注册相关"""
        username = user_info['username']
        password = user_info['password']
        # 读取userinfo文件,查看用户是否已经被注册
        td = TransferDic(socket)
        for user in HandleDb.read_file(settings.user_path):
            userinfo_list = user.split("|")
            if username == userinfo_list[0].strip():
                # 如果已经注册了就返回code
                td.send_packget_dict({"user_code": "3001"})
                return
        else:
            passwd = self.ep.md5_encry(password)
            user_msg = "%s|%s|%s"%(username, passwd, settings.disk_quotas)
            # 将用户信息写入文件
            HandleDb.write_file(settings.user_path, user_msg)
            # 帮用户以用户名创建空文件夹
            userfile_path = os.path.join(settings.home_path, username)
            os.mkdir(userfile_path)
            td.send_packget_dict({"user_code": "3002"})
            return








    def put(self):
        """上传"""
        pass

    def download(self):
        """下载"""
        pass

