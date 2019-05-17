#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
import os
import json
import traceback
import pickle
from conf import settings


class HandleDb:
    """操作数据"""
    def __init__(self, file_name):
        self.file_name = file_name


    def p_dump(self, obj):
        """将对象写入文件"""
        with open(self.file_name, 'ab') as f:
            pickle.dump(obj, f)

    def p_load(self):
        """将对象从文件中读出"""
        with open(self.file_name, 'rb') as f:
            while True:
                try:
                    obj = pickle.load(f)
                    yield obj
                except:
                    break


    def p_edit(self, obj):
        """编辑修改存储在文件中的对象"""
        f2 = HandleDb(self.file_name+".bak")    # 新建名称相同的副件
        for con_obj in self.p_load():   # 将文件内容全部读取出来
            if con_obj.name == obj.name:
                f2.p_dump(obj)
            else:
                f2.p_dump(con_obj)

        os.remove(self.file_name)
        os.rename(self.file_name+".bak", self.file_name)


    @staticmethod
    def read_db(db_path=settings.username_path):
        """直接读取文件数据"""
        try:
            f = open(db_path,"r",encoding="utf-8")
            for line in f:
                yield line
        except Exception as e:
            print(e)
            print(traceback.format_exc())
        finally:
            f.close()

    @staticmethod
    def write_db(db_value,db_path=settings.username_path):
        """写数据"""
        try:
            f = open(db_path,"a",encoding="utf-8")
            # db_value = json.dumps(db_value)
            f.write("\n"+db_value)
        except Exception as e:
            print(e)
        finally:
            f.close()
