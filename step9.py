# -*- coding: utf-8 -*-
'''
"读取沪深300指数交易数据表.xlsx",字段依次为：
Indexcd、Idxtrd01、Idxtrd05
中文名称依次为：指数代码、交易日期、收盘指数
请计算获得2016年收盘指数的10、20、30、60日移动平均收盘指数，
返回结果为(x10,x20,x30,x60)，其中xi为序列，index按年度实际交易天数从0开始编号
'''
def return_values():
    import pandas as pd
    A=pd.read_excel('沪深300指数交易数据表.xlsx')
    I1=A.iloc[:,1].values>='2016-01-01'
    I2=A.iloc[:,1].values<='2016-12-31'
    rdata=A.iloc[I1&I2,:].sort_values(['Idxtrd01'])

    #计算移动平均
    x10 = rdata['Idxtrd05'].rolling(window=10).mean()
    x20 = rdata['Idxtrd05'].rolling(window=20).mean()
    x30 = rdata['Idxtrd05'].rolling(window=30).mean()
    x60 = rdata['Idxtrd05'].rolling(window=60).mean()
    
    #索引从0开始
    x10 = x10.reset_index(drop=True)
    x20 = x20.reset_index(drop=True)
    x30 = x30.reset_index(drop=True)
    x60 = x60.reset_index(drop=True)

    return (x10,x20,x30,x60)


