# -*- coding: utf-8 -*-
'''
"读取沪深300指数交易数据表.xlsx",字段依次为：
Indexcd、Idxtrd01、Idxtrd05
中文名称依次为：指数代码、交易日期、收盘指数
分别计算2014-2017年的年度涨跌幅，
其中年度涨跌幅=（年末收盘指数-年初收盘指数）/年初收盘指数
依次返回年度涨跌幅（r1,r2,r3,r4）
'''

def rdata(date1,date2,A):
    #定义一个计算年度涨跌幅的函数
    #输入：年初日期date1、年末日期date2、交易数据A
    #返回：涨跌幅r
    
    #获取年初的收盘指数
    start_data = A[A['Idxtrd01'] >= date1].iloc[0]
    start_price = start_data['Idxtrd05']
    
    #获取年末的收盘指数
    end_data = A[A['Idxtrd01'] <= date2].iloc[-1]
    end_price = end_data['Idxtrd05']
    
    #年度涨跌幅=（年末收盘指数-年初收盘指数）/年初收盘指数
    r = (end_price - start_price) / start_price

    return r

def return_values():
    import pandas as pd
    A=pd.read_excel('沪深300指数交易数据表.xlsx')
    r1=rdata('2014-01-01','2014-12-31',A)
    r2=rdata('2015-01-01','2015-12-31',A)
    r3=rdata('2016-01-01','2016-12-31',A)
    r4=rdata('2017-01-01','2017-12-31',A)

    return (r1,r2,r3,r4)
