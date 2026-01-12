# -*- coding: utf-8 -*-
'''
基于上一关的结果，读取“上市公司财务与指标数据2013-2017.xlsx”数据，其中字段依次为：
Stkcd、Accper、B001101000	、B001300000、B001000000、B002000000、A001000000、
A001212000、F050501B、F091301A、F091001A、F090101B
中文名称依次为股票代码、会计期间、财务与指标（教材第8章中总体规模与投资效率指标）
任务为：筛选出家用电器行业股票代码2016年的财务与指标数据，字段同原数据表，记为data
'''
def return_values():
    import pandas as pd
    import step1
    r=step1.return_values()
    stkcd=list(r.index)
    


    A=pd.read_excel('上市公司财务与指标数据2013-2017.xlsx')
    A=A.iloc[A.iloc[:,1].values=='2016-12-31',:]
    data = A[A['Stkcd'].isin(stkcd)]

    return data