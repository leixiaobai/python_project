#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
import socket
import subprocess
import os
import json
import hashlib
import struct
import shutil
from conf import settings
from core.transfer_dict import TransferDic


class MyTcpClient:
    """登陆之后的操作"""
    MENU = [('put', '上传'),
            ('download', '下载'),
            ('mk_dir', '新建文件夹'),
            ('checkfile', '查看目录下的文件夹及文件'),
            ('ch_dir', '进入下一级目录'),
            ('back', '返回上一级目录'),
            ('logout', '退出')]

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    allow_reuse_address = False
    max_packet_size = 8192
    coding = 'utf-8'
    request_queue_size = 5
    # client_download_dir = 'file_download'

    def __init__(self, socket, func_str):
        self.socket = socket
        self.func_str = func_str
        self.td = TransferDic(self.socket)

    def client_close(self):
        self.socket.close()

    def run(self):
        # while True:
        if hasattr(self, self.func_str):
            func = getattr(self, self.func_str)
            func(self.func_str)

    def file_md5(self, file_path):
        """
        计算文件的md5值并返回
        :param file_path:文件路径
        :return:
        """
        md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for line in f:
                md5.update(line)
        return md5.hexdigest()

    def progress_bar(self, new_size, sum_size):
        """根据每次输入的大小判断目前的百分比"""
        bar = int(new_size / sum_size * 100)
        bar_num = bar // 3
        print("\r%s|进度为:%s%%" % ("#" * bar_num, bar), end="")

    def send_file(self, file_seek, filename, filesize):
        send_size = file_seek
        # 最后发送需要传输的文件
        with open(filename, 'rb') as f:
            f.seek(file_seek)
            for line in f:
                self.socket.sendall(line)
                # 后面发送的大小
                send_size += len(line)
                self.progress_bar(send_size, filesize)
            print()
        return send_size

    def accept_file(self, file_md5_path, old_filesize, filesize, file_md5):
        """接收服务端发送来的文件内容"""
        f = open(file_md5_path, "ab")
        recv_size = old_filesize  # 记录读取文件的大小
        while recv_size < filesize:
            recv_data = self.socket.recv(self.max_packet_size)
            file_md5.update(recv_data)
            f.write(recv_data)
            f.flush()  # 主动将内存数据写入硬盘
            recv_size += len(recv_data)
            self.progress_bar(recv_size, filesize)
        print()
        f.close()
        return recv_size,file_md5

    def put(self, action):
        """实现文件上传"""
        filename = input("输入需要上传的文件:")
        # 判断是否是文件
        if not os.path.isfile(filename):
            print('file:%s is not exists' % filename)
            return
        filesize = os.path.getsize(filename)
        file_md5_val = self.file_md5(filename)
        head_dic = {'action': action, 'filename': os.path.basename(filename), 'filesize': filesize,
                    'file_md5': file_md5_val}
        # 发送文件信息的数据字典给服务器
        self.td.send_packget_dict(head_dic)
        disk_quota = self.td.accept_packget_dict()
        disk_quota_code = disk_quota['code']
        if disk_quota_code == "1011":
            print("上传的文件超过配额")
            return
        # 接收服务端发送的数据,判断是否之前已经上传或者上传过一部分
        recv_response = json.loads(self.socket.recv(self.max_packet_size).decode(self.coding))
        file_md5_code = self.file_md5(filename)  # 先读一遍文件获取到文件的md5的值
        if recv_response['code'] == 1001:
            # 服务器无该文件,从头开始上传
            send_size = self.send_file(0, filename, filesize)
        else:
            # 移动文件的光标到上次上传的最后接着上传
            file_seek = int(recv_response['old_filesize'])
            send_size = self.send_file(file_seek, filename, filesize)
        # 发送文件的md5,判断文件一致性
        self.socket.recv(self.max_packet_size)
        self.socket.sendall(file_md5_code.encode(self.coding)) # 发送文件的md5值给服务端
        code = self.socket.recv(self.max_packet_size).decode(self.coding)
        if code == "1003":
            print("%s字节的%s文件上传成功!"%(send_size, filename))
        else:
            print("上传失败,请重新上传!")

    def download(self, action):
        """实现文件下载"""
        filename = input("输入需要下载的文件:")
        download_dir = settings.home_path
        # file_path = os.path.normpath(os.path.join(download_dir, filename))
        head_dic = {'action': action, 'filename': os.path.basename(filename) }
        self.td.send_packget_dict(head_dic)
        file_exist_code = self.td.accept_packget_dict()['code']
        if file_exist_code == "1009":
            print('file:%s is not exists' % filename)
            return
        file_dict = self.td.accept_packget_dict()
        filesize = file_dict['filesize']
        file_md5_val = file_dict['file_md5_val']
        file_md5_path = os.path.normpath(os.path.join(download_dir, file_md5_val))
        file_name_path = os.path.normpath(os.path.join(download_dir, filename))
        file_md5 = hashlib.md5()  # 计算文件的md5值,保证下载的完整性
        if not os.path.exists(file_md5_path):
            # 新文件下载
            file_dic = {'code': "1005"}  # 1005则代表该文件从未下载过
            self.td.send_packget_dict(file_dic)
            old_filesize = 0
            recv_size, file_md5 = self.accept_file(file_md5_path, old_filesize, filesize, file_md5)
        else:
            old_filesize = os.path.getsize(file_md5_path)
            # 先计算一下已经下载的部分文件的md5值
            with open(file_md5_path, "rb") as f1:
                for line in f1:
                    file_md5.update(line)
            file_dic = {'code': "1006", 'old_filesize': old_filesize}  # 1006则代表该文件下载过
            # 发送code给服务端,表示文件已经存在
            self.td.send_packget_dict(file_dic)
            recv_size, file_md5 =self.accept_file(file_md5_path, old_filesize, filesize, file_md5)

        shutil.move(file_md5_path, file_name_path)  # 把md5名称的文件改名为最终的filename
        file_md5_code = file_md5.hexdigest()  # 获取文件md5的值,字符串形式
        self.socket.sendall(file_md5_code.encode(self.coding)) # 发送文件的md5值给服务端
        code = self.socket.recv(self.max_packet_size).decode(self.coding)
        if code == "1007":
            print("%s字节的%s文件下载成功!"%(recv_size, filename))
        else:
            print("下载失败,请重新下载!")

    def mk_dir(self, action):
        """新建文件夹"""
        filename = input("目录名称:").strip()
        if not filename: return
        head_dic = {'action': action, 'filename': filename}
        self.td.send_packget_dict(head_dic)
        dir_exist_code = self.td.accept_packget_dict()['code']
        if dir_exist_code == "1013":
            print("目录已经存在")
            return
        dir_create_code = self.td.accept_packget_dict()['code']
        if dir_create_code == "1015":
            print("目录创建成功!")
            return
        else:
            print("目录创建失败!")
            return

    def checkfile(self, action):
        """查看文件夹及相关文件"""
        filename = input("输入查看的目录,.为当前目录:").strip()
        if not filename:return
        head_dic = {'action': action, 'filename': filename}
        self.td.send_packget_dict(head_dic)
        dir_msg = self.td.accept_packget_dict()
        dir_exist_code = dir_msg['code']
        if dir_exist_code == "1014":
            print("目录不存在")
            return
        dir_name = dir_msg['dir']
        dir_tree = dir_msg['dir_tree']
        print("当前%s目录下文件结构如下:"%(dir_name))
        print(dir_tree)
        return

    def logout(self, action):
        """退出"""
        quit("欢迎下次再来!")

if __name__ == '__main__':
    client1 = MyTcpClient(('127.0.0.1', 9999))
    client1.run()