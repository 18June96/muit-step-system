# -*- coding: utf-8 -*-
"""
在第一关的基础上，读取"股票交易数据_2017.xlsx"表，字段如下：
Stkcd、Trddt、Clsprc、Dnshrtrd、Dnvaltrd、Opnprc、Hiprc、Loprc，
中文名称依次为：股票代码、交易日期、收盘价、成交量、成交额、开盘价、最高价、最低价。
任务为：筛选出家电行业2017年的股票交易数据，字段同原表，记为data
"""
def return_values():
    import pandas as pd
    import step1
    r=step1.return_values()
    stkcd=list(r.index)

    A=pd.read_excel('股票交易数据_2017.xlsx')
    data = A[A['Stkcd'].isin(stkcd)]

    return data
