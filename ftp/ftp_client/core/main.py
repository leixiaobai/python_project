#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
import socket
from conf import settings
from core.transfer_dict import TransferDic
from core.client_actions import MyTcpClient


class MainFunc(object):
    """登录和注册"""
    MENU = [('login','登录'),
            ('register','注册'),
            ('logout','退出')]

    def __init__(self):
        """初始化创建socket对象"""
        self.client = socket.socket()
        self.clent_conn()
        self.coding = "utf8"

    def clent_conn(self):
        """客户端连接服务端"""
        self.client.connect(settings.ip_port)

    def send_accept_server(self, dic):
        """发送消息给服务端并接受返回数据"""
        td = TransferDic(self.client)
        td.send_packget_dict(dic)
        recv_dic = td.accept_packget_dict()
        return recv_dic

    def send_status(self, num):
        """发送status给服务端"""
        code = str(num + 2000)
        self.client.sendall(code.encode(self.coding))

    def login(self):
        """登录"""
        username = input("请输入用户名:")
        password = input("请输入密码:")
        user_info = {"username":username, "password":password}
        # 发送登录的用户信息给服务器
        recv_msg = self.send_accept_server(user_info)
        user_code = recv_msg['user_code']
        if user_code == "3003":
            print("登录成功!")
            return self.client
        else:
            print("用户名或密码有误!")

    def register(self):
        """注册"""
        username = input("请输入用户名:")
        password = input("请输入密码:")
        user_info = {"username":username, "password":password}
        # 发送注册的用户信息给服务器
        recv_msg = self.send_accept_server(user_info)
        user_code = recv_msg['user_code']
        if user_code == "3001":
            print("你输入的用户已经注册了,请重新输入!")
        else:
            print("恭喜你,注册成功!")

    @staticmethod
    def logout():
        """退出"""
        quit("欢迎下次再来!")



def run():
    """主函数"""
    print("欢迎来到xx系统".center(30,"*"))
    while True:
        for i, menu in enumerate(MainFunc.MENU, 1):
            # 打印主菜单
            print(i, menu[1])
        try:
            menu_num = int(input("请选择:"))

        except Exception:
            print("你输入的内容有误!")
            continue
        mf = MainFunc()
        # 发送操作给服务端,好让服务端判断是登陆还是注册
        mf.send_status(menu_num)
        if hasattr(mf, MainFunc.MENU[menu_num-1][0]):
            func = getattr(mf, MainFunc.MENU[menu_num-1][0])
            client = func()
            if client:
                while True:
                    # 登陆成功之后的操作
                    print("请选择菜单".center(30, "*"))
                    for i, menu in enumerate(MyTcpClient.MENU, 1):
                        # 打印主菜单
                        print(i, menu[1])
                    try:
                        menu_num = int(input("请选择:"))
                    except Exception:
                        print("你输入的内容有误!")
                        continue
                    tcp_client = MyTcpClient(client, MyTcpClient.MENU[menu_num-1][0])
                    tcp_client.run()
        else:
            print("你输入的内容不存在!")


if __name__ == '__main__':
    run()