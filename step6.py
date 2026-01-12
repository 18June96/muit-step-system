# -*- coding: utf-8 -*-
'''
在上一关基础上，构造家用电器行业交易指数，其中指数计算公式为：
当日指数=当日总交易额/基准日总交易额*100
其中当日总交易额=当日所有股票交易额之和，基准日为2017年首个交易日,
返回index_val
'''
def return_values():
    import step5
    data=step5.return_values()
   
    data_total = data.groupby('Trddt')['Dnvaltrd'].sum()

    # 获取基准日
    d = data_total.index.min()
    #交易额
    d_amount = data_total[d]
    
    # 指数=当日总交易额/基准日总交易额*100
    index_val = (data_total / d_amount * 100)

    return index_val
