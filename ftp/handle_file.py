#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
import os


class HandleFile:
    """文件操作类"""
    def __init__(self, treename='tree.txt'):
        self.treename = treename
        self.tree = ""

    def get_file_tree(self, pathname='.', n=1):
        """得到目录树结构"""
        filename = os.listdir(pathname)
        for file in filename:
            file_path = os.path.normpath(os.path.join(pathname, file))
            if os.path.isdir(file_path):
                file_tree = '   |' * n + '-' * 3 + file
                self.tree += file_tree + "\n"
                print(file_tree)
                self.get_file_tree(file_path, n + 1)
            else:
                file_tree = '   |' * n + '-' * 3 + file
                self.tree += file_tree + "\n"

                print(file_tree)

    def save_tree_file(self, pathname='.'):
        """将目录树结构写入文件中"""
        basename = os.path.basename(pathname)
        self.get_file_tree(pathname)
        with open(self.treename, 'w', encoding='utf-8') as f:
            f.write(basename+"\n")
            f.write(self.tree)

    @staticmethod
    def get_file_size(pathname):
        """获取文件夹的大小"""
        dir_size = 0
        filename = os.listdir(pathname)
        for file in filename:
            file_path = os.path.normpath(os.path.join(pathname, file))
            if os.path.isdir(file_path):
                dir_size += HandleFile.get_file_size(file_path)
            else:
                dir_size += os.path.getsize(file_path)
        return dir_size

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.abspath(__file__))
    obj = HandleFile()
    obj.save_tree_file(dir_path)
    # size = HandleFile.get_file_size(dir_path)
    # print(base_path)