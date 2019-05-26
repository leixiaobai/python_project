#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
import socket
import subprocess
import os
import json
import hashlib
import struct
import socketserver
import shutil
from conf import settings
from core.transfer_dict import TransferDic
from core.handle_file import HandleFile
from core.handle_db import HandleDb


class FtpServer():
    """文件上传下载服务端"""
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM  # tcp流类型
    allow_reuse_address = False
    max_packet_size = 8192
    coding = 'utf-8'
    request_queue_size = 5  # 队列最长数量

    def __init__(self, socket, user_info):
        self.request = socket
        self.username = user_info[0]
        self.disk_quota = int(user_info[1])*1024*1024
        self.td = TransferDic(self.request)
        self.user_dir = os.path.join(settings.home_path, self.username)


    def server_close(self):
        self.request.close()

    def close_request(self, request):
        request.close()

    def run(self):
        """服务端处理主方法"""
        while True:
            try:
                head_dic = self.td.accept_packget_dict()
                if not head_dic: return
                action = head_dic['action']
                if hasattr(self, action):
                    func = getattr(self, action)
                    func(head_dic)
            except Exception:
                return

    def file_md5_pro(self, file_path):
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
        with open(filename, "rb") as f:
            f.seek(file_seek)
            for line in f:
                self.request.send(line)
                send_size += len(line)
                self.progress_bar(send_size, filesize)
            print()
        return send_size

    def accept_file(self, file_md5_path, old_filesize, filesize):
        """接收客户端发送来的文件内容"""
        f = open(file_md5_path, "ab")
        recv_size = old_filesize  # 记录读取文件的大小
        while recv_size < filesize:
            recv_data = self.request.recv(self.max_packet_size)
            self.file_md5.update(recv_data)
            f.write(recv_data)
            f.flush()  # 主动将内存数据写入硬盘
            recv_size += len(recv_data)
            self.progress_bar(recv_size, filesize)
        print()
        f.close()
        return recv_size

    def put(self, args):
        """实现文件上传"""
        print(args)
        old_file_md5 = args['file_md5']
        filesize = args['filesize']
        filename = args['filename']
        user_dir_exist_size = HandleFile.get_file_size(self.user_dir)
        user_dir_exist_allsize = int(user_dir_exist_size) + int(filesize)
        if user_dir_exist_allsize > self.disk_quota:
            print("目前已经使用了%sMB,总共%sMB容量"%(user_dir_exist_size//1024//1024, self.disk_quota//1024//1024))
            self.td.send_packget_dict({"code":"1011"})
            return
        else:
            print("配额充足,允许上传")
            self.td.send_packget_dict({"code": "1012"})
        file_md5_path = os.path.normpath(os.path.join(self.user_dir, old_file_md5))
        file_name_path = os.path.normpath(os.path.join(self.user_dir, filename))
        # 判断文件是否之前存在
        self.file_md5 = hashlib.md5()  # 需要计算文件的md5值,保证上传的完整性
        if not os.path.exists(file_md5_path):
            old_filesize = 0
            response = {'code': 1001}  # 1001则代表是新文件
            self.request.sendall(json.dumps(response).encode(self.coding))
            recv_size = self.accept_file(file_md5_path, old_filesize, filesize)
        else:
            # 先计算一下已经上传的部分文件的md5值
            with open(file_md5_path, "rb") as f1:
                for line in f1:
                    self.file_md5.update(line)
            old_filesize = os.path.getsize(file_md5_path)
            # 1002则代表是已经存在文件,需要断点续传
            response = {'code': 1002, 'old_filesize': old_filesize}
            self.request.sendall(json.dumps(response).encode(self.coding))
            recv_size = self.accept_file(file_md5_path, old_filesize, filesize)

        shutil.move(file_md5_path, file_name_path)  # 把md5名称的文件改名为最终的filename
        file_md5_code = self.file_md5.hexdigest()  # 获取文件md5的值,字符串形式
        self.request.send(b"ok")
        recv_md5_code = self.request.recv(self.max_packet_size).decode(self.coding)  # 接收客户端发来的md5值
        if recv_md5_code == file_md5_code:
            print("%s文件上传成功,大小为%s字节!" % (filename, recv_size))
            self.request.send(b"1003")
        else:
            self.request.send(b"1004")

    def download(self, args):
        """实现文件下载"""
        filename = args['filename']
        file_path = os.path.normpath(os.path.join(self.user_dir, filename))
        if not os.path.exists(file_path):
            print('file:%s is not exists' % file_path)
            self.td.send_packget_dict({'code':"1009"})
            return
        else:
            print("1010")
            self.td.send_packget_dict({'code': "1010"})
        file_md5_code = self.file_md5_pro(file_path)
        filesize = os.path.getsize(file_path)   # 拿到服务器文件的md5值
        file_dict = {'filesize':filesize,'file_md5_val':file_md5_code}
        # 发送服务端文件的大小
        self.td.send_packget_dict(file_dict)
        # 接收code,看文件是否被下载过
        file_dic = self.td.accept_packget_dict()
        exist_code = file_dic['code']
        # 接下来传输文件
        if exist_code == "1005":
            # 1005 表示客户端无该文件,全新下载
            send_size = self.send_file(0, file_path, filesize)
        else:
            old_filesize = file_dic['old_filesize']
            f_seek = old_filesize  # 文件读取的偏移量
            send_size = self.send_file(f_seek, file_path, filesize)
        # 发送文件的md5,判断文件一致性
        file_md5_client = self.request.recv(self.max_packet_size).decode(self.coding)
        if file_md5_client == file_md5_code:
            print("%s文件下载成功,大小为%s字节!" % (filename, send_size))
            self.request.send(b"1007")
        else:
            self.request.send(b"1008")


    def mk_dir(self, args):
        """新建文件夹"""
        filename = args['filename']
        file_path = os.path.normpath(os.path.join(self.user_dir, filename))
        if os.path.exists(file_path):
            self.td.send_packget_dict({"code":"1013"})
            print("%s目录已经存在"%filename)
            return
        else:
            self.td.send_packget_dict({"code": "1014"})
        try:
            os.mkdir(file_path)
            self.td.send_packget_dict({"code": "1015"})
            print("创建目录成功")
            return
        except:
            self.td.send_packget_dict({"code": "1015"})
            print("创建目录失败")
            return

    def checkfile(self, args):
        """查看文件夹及相关文件"""
        filename = args['filename']
        if filename == ".":
            file_path = self.user_dir
        else:
            file_path = os.path.normpath(os.path.join(self.user_dir, filename))
            print(file_path)
        if os.path.exists(file_path):
            hf = HandleFile()
            hf.get_file_tree(file_path)
            self.td.send_packget_dict({"code":"1013", "dir":os.path.basename(file_path),"dir_tree":hf.tree})
        else:
            self.td.send_packget_dict({"code": "1014"})


if __name__ == '__main__':
    ip_port = ('127.0.0.1', 9999)
    server = socketserver.ThreadingTCPServer(ip_port, FtpServer)
    server.serve_forever()
