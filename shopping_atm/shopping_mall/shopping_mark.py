# -*- coding:utf-8 -*-
# @__author__ : Loris
# @Time : 2018/10/24 9:11
"""
当前未与ATM相结合，后续用接口方式实现扣钱
"""

import os
import sys

def second_shopping_car():
    #商品列表，这里就将商品和价格用元组表示
    shops_list = [
        ("iphoneX", 12800),
        ("Book", 100),
        ("Computer", 5000),
        ("Flower", 99),
         ("Tea", 35),
    ]

    #用户账户余额
    salary = 10000

    #用户购物车列表
    buy_shops = []

    while True:
        #展示所有商品信息
        for num, shop in enumerate(shops_list, 1):
            if num == 1:
                print("序号".ljust(8)+"商品".ljust(10)+"价格".ljust(10))
            print(str(num).ljust(10)+shop[0].ljust(12)+str(shop[1]).ljust(10))

        #接收用户输入要购买的商品
        shop_num =  input("请您选择商品，退出请输入quit：")

        #判断输入是否合理
        if shop_num.isdigit():
            shop_num = int(shop_num)
            if shop_num>0 and shop_num<=len(shops_list):
                #当前商品
                current_shop = shops_list[shop_num-1]

                #判断余额是否大于当前商品的价格，大于则加入购物车，小于则提示余额不足
                if current_shop[1] <= salary:
                    salary -= current_shop[1] #减去商品的价格
                    #如果说购物车有商品则将商品拿出来依次判断
                    if len(buy_shops) != 0:
                        for buy_shop in buy_shops:
                            if current_shop[0] == buy_shop[0]:
                                 #当发现有同样商品时，商品数量加1，然后退出循环
                                buy_shop[1] += 1
                                break
                        #当循环完成后如果还是没有找到相同的商品，则额外添加商品，数量默认为1
                        else:
                            buy_shops.append([current_shop[0], 1])
                    #如果没商品就直接添加第一个
                    else:
                        buy_shops.append([current_shop[0], 1])  #将商品加入到购物车
                    print("您已将%s商品加入购物车，当前账户余额为%d"%(current_shop[0], salary))
                else:
                    print("您当前余额不足，还剩%s元钱"%salary)
            else:
                print("你输入的商品序号不存在，请重新输入！")
        elif shop_num == "quit":
            #在退出前展示已购买列表
            print("--------已购买商品列表如下--------")
            print("商品".ljust(8)+"数量".ljust(10))
            for buy_shop in buy_shops:
                print(buy_shop[0].ljust(10)+str(buy_shop[1]).ljust(10))

            break
        else:
            print("你输入的内容有误，请重新输入！")

if __name__ == "__main__":
    second_shopping_car()