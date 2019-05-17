#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei


class School(object):
    """学校类"""
    def __init__(self, name):
        """
        :param name:学校名称
        """
        self.name = name



class Grade(object):
    """班级类"""
    def __init__(self, name, school, course):
        """
        :param name:班级名称
        :param school: 班级所属学校
        :param course: 班级的课程
        :param student: 班级学生的对象
        """
        self.name = name
        self.school = school
        self.course = course
        self.student = []
        # self.student_path = student_path


class Course(object):
    """
    课程相关信息
    """
    def __init__(self, name,school, price, period):
        """
        初始化课程
        :param name:课程名称
        :param price: 课程价格
        :param period: 课程周期
        :param school: 所属学校
        """
        self.name = name
        self.school = school
        self.price = price
        self.period = period
