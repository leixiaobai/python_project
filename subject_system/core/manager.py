#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
import sys
import os

top_path = os.path.dirname(os.path.dirname(__file__))  # 最顶层目录路径
sys.path.append(top_path)  # 加入到系统路径,方便模块导入
from core.handle_db import HandleDb
from conf import settings
from core.education import School, Grade, Course
from core.teacher import Teacher
from core.student import Student


class Manager(object):
    """管理员角色"""
    menu = [("create_school", "创建学校"),
            ("create_cource", "创建课程"),
            ("create_grade", "创建班级"),
            ("create_student", "创建学生"),
            ("create_teacher", "创建讲师"),
            ("show_cources", "查看课程"),
            ("show_grades", "查看班级"),
            ("show_teacher", "查看讲师"),
            ("bound_grade_teacher", "为班级指定老师"),
            ("exit", "退出")]

    def __init__(self, name):
        """
        :param name:管理员名称
        """
        self.name = name
        self.teacher_pickle_obj = HandleDb(settings.teacher_obj)
        self.student_pickle_obj = HandleDb(settings.student_obj)
        self.school_pickle_obj = HandleDb(settings.school_obj)
        self.course_pickle_obj = HandleDb(settings.course_obj)
        self.grade_pickle_obj = HandleDb(settings.grade_obj)

    def create_school(self):
        """创建学校"""
        print("目前已经存在的课程有:")
        for i, school_obj in enumerate(self.school_pickle_obj.p_load(), 1):  # 读取目前存在的学校
            print(i, school_obj.name)
        school_name = input("请输入需要创建的学校,b返回上一步:")
        if school_name.upper() == "B":
            return
        for school_obj in self.school_pickle_obj.p_load():
            if school_name == school_obj.name:
                print("你输入的学校已存在,请重新输入!")
                break
        else:
            self.school_pickle_obj.p_dump(School(school_name))  # 将学校对象写入文件
            print("创建学校成功!")

    def create_cource(self):
        """创建课程"""
        self.show_cources()
        course_name = input("请输入需要创建的课程名称,返回请输入b:")
        if course_name.upper() == "B":
            return
        course_school = input("请输入创建的课程所属学校:")
        for school_obj in self.school_pickle_obj.p_load():
            if course_school == school_obj.name:
                break  # 证明输入的校区存在
        else:
            print("你输入的校区不存在,请重新输入")
            return

        for course_obj in self.course_pickle_obj.p_load():
            if course_name == course_obj.name and course_school == course_obj.school:
                print("你输入的课程已存在该校区,请重新输入!")
                break
        else:
            course_price = input("请输入课程价格:")
            course_period = input("请输入课程周期:")
            self.course_pickle_obj.p_dump(Course(course_name, course_school, course_price, course_period))
            print("创建课程成功!")

    def create_grade(self):
        """创建班级"""
        self.show_grades()
        grade_name = input("请输入需要创建的班级名称,返回请输入b:")
        if grade_name.upper() == "B":
            return

        grade_school = input("请输入创建的班级所属学校:")
        for school_obj in self.school_pickle_obj.p_load():
            if grade_school == school_obj.name:
                break  # 证明输入的校区存在
        else:
            print("你输入的校区不存在,请重新输入")
            return
        grade_course = input("请输入创建的班级课程:")
        for course_obj in self.course_pickle_obj.p_load():
            if grade_course == course_obj.name:
                break  # 证明输入的课程存在
        else:
            print("你输入的课程不存在,请重新输入")
            return
        for grade_obj in self.grade_pickle_obj.p_load():
            if grade_name == grade_obj.name and grade_school == grade_obj.school and grade_course == grade_obj.course:
                print("你输入的班级,所属校区及课程完全一样,请重新输入!")
                break
        else:
            self.grade_pickle_obj.p_dump(Grade(grade_name, grade_school, grade_course))
            print("创建班级成功!")

    def create_teacher(self):
        """创建老师"""
        teacher_name = input("请输入要创建的老师名称,返回请输入b:")
        if teacher_name.upper() == "B":
            return
        teacher_passwd = input("请输入要创建的老师的密码:")
        for i, school_obj in enumerate(self.school_pickle_obj.p_load(), 1):  # 读取目前存在的学校
            print(i, school_obj.name)
        teacher_school = input("请输入老师所属学校:")
        for school_obj in self.school_pickle_obj.p_load():  # 读取目前存在的学校
            if teacher_school == school_obj.name:
                break
        else:
            print("你输入的学校不存在,请重新输入!")
            return
        teacher_msg = "%s|%s|1" % (teacher_name, teacher_passwd)
        HandleDb.write_db(teacher_msg)  # 将账号写入用户信息文件
        self.teacher_pickle_obj.p_dump(Teacher(teacher_name, teacher_school))
        print("创建老师成功!")

    def create_student(self):
        """创建学生"""
        student_name = input("请输入要创建的学生名称,返回请输入b:")
        if student_name.upper() == "B":
            return
        student_passwd = input("请输入要创建的学生的密码:")
        for i, school_obj in enumerate(self.school_pickle_obj.p_load(), 1):  # 读取目前存在的学校
            print(i, school_obj.name)
        student_school = input("请输入学生所属学校:")
        for school_obj in self.school_pickle_obj.p_load():  # 读取目前存在的学校
            if student_school == school_obj.name:
                break
        else:
            print("你输入的学校不存在,请重新输入!")
            return
        is_grade = input("是否需要现在为学生分配班级,y or n:")
        if is_grade.upper() == "Y":
            student_grade = input("请输入学生所属班级:")
            for grade_obj in self.grade_pickle_obj.p_load():  # 读取目前存在的班级
                if student_grade == grade_obj.name:
                    break
            else:
                print("你输入的班级不存在,请重新输入!")
                return
            student_msg = "%s|%s|2" % (student_name, student_passwd)
            HandleDb.write_db(student_msg)  # 将账号写入用户信息文件
            # 修改班级中学生的属性,将学生加入到班级中
            # grade_stu = self.grade_pickle_obj.p_load()
            grade_obj_tem = None
            for grade_obj in self.grade_pickle_obj.p_load():
                if grade_obj.name == student_grade:
                    grade_obj.student.append(student_name)
                    grade_obj_tem = grade_obj
            if grade_obj_tem:
                self.grade_pickle_obj.p_edit(grade_obj)
                self.student_pickle_obj.p_dump(
                    Student(student_name, student_school, student_grade))  # 将学生对象写入了文件,但是这里还关联了班级,所以需要修改保存班级的对象文件
                print("创建学生成功!")
                return
        elif is_grade.upper() == "N":
            student_msg = "%s|%s|2" % (student_name, student_passwd)
            HandleDb.write_db(student_msg)  # 将账号写入用户信息文件
            self.student_pickle_obj.p_dump(Student(student_name, student_school))
            print("创建学生成功!")
        else:
            print("输入有误,请重新输入!")
            return

    def show_cources(self):
        """查看所有课程"""
        print("展示:课程,校区:")
        print("-" * 50)
        for i, course_obj in enumerate(self.course_pickle_obj.p_load(), 1):
            print(i, course_obj.name, course_obj.school)
        print("-" * 50)

    def show_grades(self):
        """查看班级"""
        print("展示:班级,校区,课程,班级学生:")
        print("-" * 50)
        for i, grade_obj in enumerate(self.grade_pickle_obj.p_load(), 1):
            print(i, grade_obj.name, grade_obj.school, grade_obj.course, grade_obj.student)
        print("-" * 50)

    def show_teacher(self):
        """查看老师"""
        print("展示:老师,校区,班级:")
        print("-" * 50)
        for i, teacher_obj in enumerate(self.teacher_pickle_obj.p_load(), 1):
            print(i, teacher_obj.name, teacher_obj.school, teacher_obj.grade)
        print("-" * 50)

    def bound_grade_teacher(self):
        """为班级指定老师"""
        self.show_grades()
        grade_name = input("请输入要指定的班级")
        for grade_obj in self.grade_pickle_obj.p_load():  # 读取目前存在的班级
            if grade_name == grade_obj.name:
                break
        else:
            print("你输入的班级不存在,请重新输入!")
            return
        teacher_name = input("请输入要指定的老师")
        teacher_obj_tem = None
        for teacher_obj in self.teacher_pickle_obj.p_load():
            if teacher_name == teacher_obj.name:
                teacher_obj.grade.append(grade_name)
                teacher_obj_tem = teacher_obj
        if teacher_obj_tem:
            self.teacher_pickle_obj.p_edit(teacher_obj_tem)
            print("为班级指定老师成功")
            return
        else:
            print("你输入的老师不存在,请重新输入!")
            return

    def exit(self):
        """退出"""
        exit("程序退出,欢迎下次再来!")


if __name__ == '__main__':
    m = Manager('admin')
    m.create_student()
