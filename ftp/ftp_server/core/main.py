#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
import socketserver

from conf import settings
from core.transfer_dict import TransferDic
from core.actions import Action
from core.servers import FtpServer


class MyServer(socketserver.BaseRequestHandler):
    """主函数执行的主要内容"""
    def handle(self):
        """
        服务端处理主方法
        self.request 是客户端的socket对象
        :return:
        """
        print(self.client_address)
        status = self.request.recv(8096)    # 接收客户端的操作
        if status == b"2003":
            self.request.close()
            return
        # 从字典中取出方法
        func_str = settings.status.get(status.decode('utf8'))
        td = TransferDic(self.request)
        # 接收客户端的信息
        user_info = td.accept_packget_dict()

        action = Action()
        if hasattr(action, func_str):
            func = getattr(action, func_str)
            user_info = func(self.request, user_info)
            if user_info:
                # 登陆成功之后的操作
                tcp_server = FtpServer(self.request, user_info)
                tcp_server.run()



def run():
    """主函数"""
    server = socketserver.ThreadingTCPServer(settings.ip_port, MyServer)
    server.serve_forever()
