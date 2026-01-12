# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
'''
"读取沪深300指数交易数据表.xlsx",字段依次为：
Indexcd、Idxtrd01、Idxtrd05
中文名称依次为：指数代码、交易日期、收盘指数
请计算获得2016年收盘指数的现价指标，其公式为：
现价=当日收盘指数 / 过去 10 个交易日的移动平均收盘指数
返回结果为p10，为序列，index按年度实际交易天数从0开始编号
'''
def return_values():
    import pandas as pd
    A=pd.read_excel('沪深300指数交易数据表.xlsx')
    I1=A.iloc[:,1].values>='2016-01-01'
    I2=A.iloc[:,1].values<='2016-12-31'
    rdata=A.iloc[I1&I2,:].sort_values(['Idxtrd01'])

    #10日移动平均收盘指数
    ma10 = rdata['Idxtrd05'].rolling(window=10).mean()
    
    #现价=当日收盘指数 / 过去 10 个交易日的移动平均收盘指数
    p10 = rdata['Idxtrd05'] / ma10
    
    #重置索引，drop=True——去掉原先索引
    p10 = p10.reset_index(drop=True)   #reset_index()——重置索引

    return p10



