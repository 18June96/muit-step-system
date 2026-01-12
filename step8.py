# -*- coding: utf-8 -*-
'''
序列x1,x2,x3,如果|x2-(x1+x2)/2|越大，x2成为关键转折点的可能性就越大。
"读取沪深300指数交易数据表.xlsx",字段依次为：
Indexcd、Idxtrd01、Idxtrd05
中文名称依次为：指数代码、交易日期、收盘指数
请计算获得2016年指数的关键转折点20个，包括年初和年末的两个点。
并输出结果，用一个序列Fs来表示，其中index为序号，值为收盘指数。
注意：序号按年度实际交易日期从0开始编号
'''
def return_values():
    import pandas as pd
    import numpy as np
    A=pd.read_excel('沪深300指数交易数据表.xlsx')
    I1=A.iloc[:,1].values>='2016-01-01'
    I2=A.iloc[:,1].values<='2016-12-31'
    data=A.iloc[I1&I2,:].sort_values(['Idxtrd01'])

    turn_points = []
    p = data['Idxtrd05'].values  #价格
    
    for i in range(1, len(p) - 1):
        #转折点 |x2-(x1 + x3)/2|
        a = abs(p[i] - (p[i-1] + p[i+1]) / 2)  
        turn_points.append((i,a,p[i]))
    
    #转折18个点，加上首尾就20个
    turn_points.sort(key=lambda x: x[1], reverse=True)
    sel_points = turn_points[:18]

    # 提取索引
    sel_i = []
    for point in sel_points:
        sel_i.append(point[0])

    #提取价格
    sel_p = []
    for point in sel_points:
        sel_p.append(point[2])
  
    #添加首尾两个点
    sel_i = [0] + sel_i + [len(p)-1]
    sel_p = [p[0]] + sel_p + [p[-1]]
    
    #创建keydata序列
    keydata = pd.Series(sel_p, index=sel_i)

    return keydata