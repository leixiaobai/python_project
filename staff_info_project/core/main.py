#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Xiaobai Lei
'''程序的主入口'''
from core.select_operate import select
from core.create_operate import create
from core.delete_operate import delete
from core.update_operate import update


def main():
    '''主函数,程序入口'''
    operate_lst = ['查询','新增','删除','修改']     # 用户操作选择列表
    operate_func = ['select', 'create', 'delete', 'update']     # 将操作的对应函数名称写在列表中方便调用
    for index, operate in enumerate(operate_lst, 1):    # 展示操作选项让用户选择,从1开始
        print(index,operate)
    try:        # 捕捉用户输入的异常
        operate_choice_num = int(input("请选择需要操作的编号:").strip())
    except ValueError:
        print("你输入的有误,请输入数字!")
    except Exception as e:
        print(e)
    else:
        if operate_choice_num in list(range(1,len(operate_func)+1)):
            eval(operate_func[operate_choice_num-1])()     # 执行对应程序代码,增删改查
        else:
            print("请输入指定的数字编号,不能大于%d"%len(operate_func))




if __name__ == '__main__':
    main()



