#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
from core.handle_db import HandleDb
from conf import settings


class Teacher:
    """教师类"""
    menu = [("show_my_grades", "查看自己教学的班级"),
            ("show_my_cources", "查看自己教的课程"),
            ("exit", "退出")]

    def __init__(self, name, school=None):
        """
        :param name: 讲师名称
        :param school: 老师所属学校
        """
        self.name = name
        self.school = school
        self.grade = []
        self.teacher_pickle_obj = HandleDb(settings.teacher_obj)
        self.grade_pickle_obj = HandleDb(settings.grade_obj)

    def show_my_grades(self):
        """查看自己教学的班级"""
        print("班级如下:")
        print("-" * 50)
        for teacher_obj in self.teacher_pickle_obj.p_load():
            if teacher_obj.name == self.name:
                self.grade = teacher_obj.grade
                break
        for i, grade in enumerate(self.grade, 1):
            print(i, grade)
        print("-" * 50)

    def show_my_cources(self):
        """查看自己教的课程"""
        print("课程如下:")
        print("-" * 50)
        for grade_obj in self.grade_pickle_obj.p_load():
            for i, grade in enumerate(self.grade, 1):
                if grade_obj.name == grade:
                    print(i, grade_obj.course)
        print("-" * 50)

    def exit(self):
        """退出"""
        exit("程序退出,欢迎下次再来!")
