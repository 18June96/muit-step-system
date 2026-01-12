# 多步骤分析系统设计与实现技术文档
## 一、项目概述
　　本系统是一个集成化的金融数据实验平台，主要用于演示和执行一系列与股票市场分析相关的数据处理任务。系统采用 Streamlit 作为前端框架，允许用户通过侧边栏选择不同的实验模块，动态加载并展示代码、原始数据及计算结果。
## 二、技术架构
　　核心框架: **Streamlit** (用于构建 Web 交互界面)  
　　数据处理: **Pandas** (用于数据读取、清洗和分析)  
　　可视化: **Matplotlib** (用于绘制金融走势图)  
　　代码组织: **模块化编程** (将不同功能拆分为独立文件)  
## 三、文件结构
　　step1.py 至 step10.py	————存放具体的业务逻辑和计算函数，被主程序动态导入；  
　　申万行业分类.xlsx	————存储股票代码与所属行业的映射关系；  
　　上市公司财务与指标数据2013-2017.xlsx	————存储公司的财务指标数据；  
　　股票交易数据_2017.xlsx	————存储 2017 年的股票交易记录；  
　　沪深300指数交易数据表.xlsx	————存储沪深300指数的历史交易数据。  
　　**数据来源**：tushre数据https://tushare.pro/
## 四、核心功能详解
系统通过侧边栏菜单驱动，共包含 10 个 主要实验模块。  
### 4.1 模块 1-4：数据获取与财务分析
这部分主要关注于**申万家用电器行业**的数据处理。  
#### 模块 1: 申万家用电器行业股票代码获取  
　　功能: 读取行业分类表，提取属于“家用电器”行业的所有股票代码及简称。  
　　数据源: 申万行业分类.xlsx  
　　输出: 股票代码与简称的对应列表。  
```python
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
```
#### 模块 2: 申万家用电器行业股票财务指标数据获取  
　　功能: 从庞大的财务数据库中筛选出特定行业的财务数据。  
　　数据源: 上市公司财务与指标数据2013-2017.xlsx  
　　输出: 原始财务指标数据集。  
```python
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
```
#### 模块 3: 申万家用电器行业股票财务指标数据处理  
　　功能: 对原始财务数据进行清洗、标准化或特征提取（具体逻辑取决于 step3.py 内容）。  
　　输入: 模块 2 的输出结果。  
　　输出: 处理后的数值矩阵及对应的股票代码。  
```python
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
```
#### 模块 4: 主成分累计贡献率在95%  
　　功能: 应用主成分分析技术，确定能够解释 95% 数据方差所需的主成分数量。  
　　输入: 模块 3 处理后的数据。  
　　输出: 主成分分析结果（如特征值、贡献率等）。  
```python
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
```
### 4.2 模块 5-6：家电行业交易分析  
这部分专注于家电行业的**市场交易行为**分析。  
#### 模块 5: 家电行业2017年的股票交易数据  
　　功能: 读取并展示 2017 年的交易数据，并绘制前 5 只股票的收盘价走势图。  
　　数据源: 股票交易数据_2017.xlsx  
　　可视化: 使用 Matplotlib 绘制多条折线图，展示不同股票的价格趋势。  
```python
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
```
#### 模块 6: 家用电器行业交易指数  
　　功能: 计算并展示该行业的综合交易指数走势。  
　　可视化: 绘制行业指数随时间变化的折线图，X 轴按月显示。  
```python
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
```
### 4.3 模块 7-10：沪深300指数技术分析  
这部分专注于**沪深300指数**的**技术指标计算与分析**。  
#### 模块 7: 沪深300指数年度涨跌幅  
　　功能: 计算沪深300指数每年的涨跌幅情况。  
　　数据源: 沪深300指数交易数据表.xlsx  
```python
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
```
#### 模块 8: 沪深300指数2016年指数的关键转折点  
　　功能: 识别并标记 2016 年指数走势中的关键转折点（如波峰波谷）。  
　　可视化: 在指数走势图上用红色散点标出转折点位置。  
```python
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
```
#### 模块 9: 沪深300指数2016年平均收盘  
　　功能: 计算不同周期（如 10日、20日、60日）的移动平均线。  
　　可视化: 绘制指数收盘价与多条均线的叠加图，用于观察趋势支撑与压力。  
```python
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
```
#### 模块 10: 沪深300指数2016年收盘指数的现价指标  
功能: 计算与收盘价相关的技术指标（如乖离率、动量等，具体取决于 step10.py 逻辑）。  
```python
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
```
## 五、关键代码逻辑分析
1. 动态代码加载  
系统通过读取 .py 文件的内容，并使用 st.code() 在网页上展示源代码，实现了“代码可见”的教学目的。
```python
def get_file_content(file_path):
    # ... 打开并读取文件 ...
    return f.read()
# 在界面中展示
st.code(s1, language='python') 
```
2. 模块化导入  
代码使用了 import step1, step2... 的方式动态导入模块，并调用各模块中定义的 return_values() 函数来获取计算结果。这要求每个 stepX.py 文件必须定义一个 return_values 函数。
```python
import step1,step2,step3,step4,step5,step6,step7,step8,step9,step10
#读取多个.py文件
file = ['step1.py','step2.py','step3.py','step4.py','step5.py','step6.py','step7.py','step8.py','step9.py','step10.py',]

def get_file_content(file_path):
    for file_path in file:
        with open(file_path, "r",encoding="utf-8") as f:
            return f.read()

#获取.py文件内容
s1 = get_file_content("step1.py")
s2 = get_file_content("step2.py")
s3 = get_file_content("step3.py")
s4 = get_file_content("step4.py")
s5 = get_file_content("step5.py")
s6 = get_file_content("step6.py")
s7 = get_file_content("step7.py")
s8 = get_file_content("step8.py")
s9 = get_file_content("step9.py")
s10 = get_file_content("step10.py")
```
4. 数据可视化处理  
在绘制金融图表时，代码处理了中文显示问题（设置 SimHei 字体）和日期格式问题，确保图表在 Streamlit 中正确渲染。
```python
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
```
## 六、高级可视化子系统
### 6.1 step5：股票走势可视化
　　多只股票对比，采用多线图，每条线代表一只股票，数据自动选取前5只股票，避免图表过于拥挤；使用groupby按股票代码分组绘制。
<img width="1860" height="843" alt="image" src="https://github.com/user-attachments/assets/4dbcd882-cd9c-4492-8614-8854c0c327d2" />
```python
elif step_num == 5:
    # 数据处理
    df['Trddt'] = pd.to_datetime(df['Trddt'], format='%Y-%m-%d')
    
    # 可视化配置
    plt.rcParams['font.sans-serif'] = 'SimHei'
    st.subheader('可视化走势图 ')
    top5_stocks = df['Stkcd'].unique()[:5]  # 只显示前5只股票
    plot_data = df[df['Stkcd'].isin(top5_stocks)]
    
    # 多线图绘制
    plt.figure(figsize=(10, 5))
    for code, group in plot_data.groupby('Stkcd'):
        plt.plot(group['Trddt'], group['Clsprc'], markersize=3, label=str(code))
```
### 6.2 step6：行业指数可视化
　　单一指数走势，采用单线图，重点是时间序列模式。
<img width="1860" height="855" alt="image" src="https://github.com/user-attachments/assets/063fa83e-0ddd-47c1-9fa0-0abc922e632c" />
```python
# 专业的时间序列处理
df['Trddt'] = pd.to_datetime(df['Trddt'], format='%Y-%m-%d')  
df = df.sort_values('Trddt')  # 按日期排序
plt.rcParams['font.sans-serif'] = 'SimHei'
 
# 创建图表对象
fig, ax = plt.subplots(figsize=(12, 6))
 
# 绘制指数走势（限制前501个数据点）
ax.plot(df['Trddt'][:501], df['行业指数'][:501], linewidth=2, color='blue', label='指数走势')
 
# 专业的时间轴格式化
ax.xaxis.set_major_locator(mdates.MonthLocator())  # 按月设置刻度
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # 格式为年月
```
### 6.3 step8：转折点分析可视化
　　关键点位识别，采用折线+散点图，突出特殊点位。
<img width="1860" height="839" alt="image" src="https://github.com/user-attachments/assets/f17ad374-c374-47e8-a9e9-bb07a63d00d7" />
```python
# 数据准备
rdata['交易天数'] = range(len(rdata))  # 创建连续的交易天数序列
 
# 中文显示配置
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
 
# 绘制基础折线图
ax.plot(rdata['交易天数'], rdata['Idxtrd05'], 'b-', alpha=0.9, label='指数序列', linewidth=1.2)
 
# 高亮转折点
ax.scatter(r.index, r.values, color='red', s=25, edgecolor='black', linewidth=0.8, zorder=5, label='转折点')    # zorder=5确保散点图在折线图上方
 
# 样式优化
ax.spines['top'].set_visible(False)  # 隐藏上边框
ax.spines['right'].set_visible(False)  # 隐藏右边框
```
### 6.4 step9：移动平均线可视化
　　多周期分析，采用多线叠加图，展示不同周期的趋势。
<img width="1860" height="905" alt="image" src="https://github.com/user-attachments/assets/b5883d08-72e7-4c81-b9c0-59da1aba6f2e" />
```python
# 多线图绘制（4条移动平均线）
plt.plot(rdata['Idxtrd01'], x10, label='10日移动平均', linewidth=1, color='blue')
plt.plot(rdata['Idxtrd01'], x20, label='20日移动平均', linewidth=1, color='orange')
plt.plot(rdata['Idxtrd01'], x30, label='30日移动平均', linewidth=1, color='green')
plt.plot(rdata['Idxtrd01'], x60, label='60日移动平均', linewidth=1, color='red')
 
# 图表样式配置
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.title('2016年沪深300指数移动平均线', fontsize=14)
plt.ylabel('指数点位', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.2)  # 半透明网格
plt.xticks(rotation=45)  # x轴标签旋转45度
```
## 七、Streamlit网页面部分展示
<img width="1533" height="2062" alt="image" src="https://github.com/user-attachments/assets/919c77a1-b14a-4f75-b555-9b6a8a88f477" />

## 八、注意事项
　　数据完整性: 所有 Excel 数据文件必须与 Python 脚本位于同一目录下，否则会报错。  
　　模块依赖: 如果 step1.py 到 step10.py 中的函数逻辑发生改变（例如 return_values 函数名更改），主程序将无法正常运行。  
　　性能优化: 当前代码在每次选择菜单时都会重新读取 Excel 文件，对于大文件可能会有卡顿。在生产环境中，建议使用 @st.cache_data 装饰器来缓存数据读取结果。  
## 九、总结
　　这个项目展示了如何将复杂的金融数据分析任务分解为清晰的步骤，并通过现代化的Web界面呈现，是一个功能完整的分析工具，涵盖数据科学项目从数据处理到结果展示的全过程；这个系统可以作为金融数据分析的入门项目，也可以作为企业级分析工具的雏形进行进一步开发。
