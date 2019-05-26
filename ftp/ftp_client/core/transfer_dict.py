#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
import json
import struct


class TransferDic(object):
    """传输(发送和接收)字典数据,避免黏包出现"""
    def __init__(self, socket):
        self.socket = socket
        self.coding = "utf8"

    def send_packget_dict(self, head_dic):
        """打包文件基本信息字典发送给服务端"""
        # 先计算文件的md5的值
        head_json = json.dumps(head_dic)
        head_json_bytes = head_json.encode(self.coding)
        head_struct = struct.pack("i", len(head_json_bytes))
        # 先发送字典数据的pack字节
        self.socket.sendall(head_struct)
        # 接着发送字典数据
        self.socket.sendall(head_json_bytes)

    def accept_packget_dict(self):
        """接收服务端发送的数据字典"""
        head_struct = self.socket.recv(4)
        if not head_struct: return
        head_len = struct.unpack('i', head_struct)[0]
        head_json = self.socket.recv(head_len).decode(self.coding)
        head_dic = json.loads(head_json)
        return head_dic