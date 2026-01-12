# -*- coding: utf-8 -*-
#1.读取“申万行业分类.xlsx”表，字段如下所示：
# 行业名称    股票代码    股票名称
# 获得“家用电器”行业的所有上市公司股票代码和股票简称
# 结果用序列Fs来表示，其中index为股票代码、值为股票简称
def return_values():
    import pandas as pd
    A=pd.read_excel('申万行业分类.xlsx')
    F = A[A['行业名称']=='家用电器']
    Fs = pd.Series(F['股票名称'].values,index=F['股票代码'])

    return Fs
