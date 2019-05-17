#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei


class Student(object):
    """学生相关信息"""
    menu = [("select_cource", "选择课程"),
            ("show_cource", "查看所选课程"),
            ("show_all_cource", "查看所有课程"),
            ("delete_cource", "删除课程"),
            ("exit", "退出")]


    def __init__(self, name, school=None, grade=None):
        """
        :param name:学生姓名
        :param school:学生所在的学校
        :param grade:学生所在的班级
        """
        self.name = name
        self.school = school
        self.grade = grade

    def select_cource(self):
        """选择课程"""
        pass

    def show_cource(self):
        """查看所选课程"""
        pass

    def show_all_cource(self):
        """查看所有课程"""
        pass

    def delete_cource(self):
        """查看所选课程"""
        pass

    def exit(self):
        """退出"""
        exit("程序退出,欢迎下次再来!")