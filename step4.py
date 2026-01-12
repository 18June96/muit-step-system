# -*- coding: utf-8 -*-
'''
在上一关基础上，对去掉缺失值和标准化后的x，进行主成分分析，
并提取主成分，要求累计贡献率在95%
'''
def return_values():
    import step3
    from sklearn.decomposition import PCA
    
    r = step3.return_values()
    x = r[0]

    #导入主成分分析模块PCA
    #创建分析对象y
    y = PCA(n_components=0.95)  #贡献率为0.95
    y.fit(x)   #对待分析的数据进行拟合训练
    Y = y.transform(x)   #返回提取的主成分

    return Y
