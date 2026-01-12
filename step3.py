# -*- coding: utf-8 -*-
'''
在上一关基础上，对筛选出的家用电器行业股票代码2016年的财务与指标数据，
去掉空缺值、作均值-方差标准化处理，返回结果x（数组）和股票代码code(列表)
'''
def return_values():
    import step2
    data=step2.return_values() #上一关的结果，家用电器行业股票代码2016年的财务与指标数据
    data = data.dropna()  #删除缺失值
    code = data['Stkcd'].tolist()   #转化为列表.tolist()
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()   #创建对象

     # 提取所有数值列
    num = data.select_dtypes(include=['number'])
    x = num.values   # 直接获取数值数组

    scaler.fit(x)   #调用fit()拟合方法
    x = scaler.transform(x)
    
    return (x,code)

