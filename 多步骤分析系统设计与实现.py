import streamlit as st
import step1,step2,step3,step4,step5,step6,step7,step8,step9,step10
import pandas as pd
import matplotlib.pyplot as plt

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

st.set_page_config(
            page_title="03_谢卓君",  # 页面标题
            layout='wide',
        )

with st.sidebar:
     st.subheader('请选择实验')
     List=['1.申万家用电器行业股票代码获取',
           '2.申万家用电器行业股票财务指标数据获取',
           '3.申万家用电器行业股票财务指标数据处理',
           '4.主成分累计贡献率在95%',
           '5.家电行业2017年的股票交易数据',
           '6.家用电器行业交易指数',
           '7.沪深300指数年度涨跌幅',
           '8.沪深300指数2016年指数的关键转折点',
           '9.沪深300指数2016年平均收盘',
           '10.沪深300指数2016年收盘指数的现价指标']
     nm=st.selectbox(" ",List)
     
if nm=='1.申万家用电器行业股票代码获取':
    st.subheader('//申万家用电器行业股票代码获取//')
    st.subheader('原始数据（取前100条） =====')
    ss1 = pd.read_excel('申万行业分类.xlsx')
    st.dataframe(ss1.head(100),use_container_width=True)
    
    st.subheader('代码 =====')
    st.code(s1,language='python')
   
    st.subheader('结果框 =====')
    r=step1.return_values()
    st.dataframe(pd.DataFrame({'股票代码':list(r.index),'股票简称':r.values}))
     
if nm=='2.申万家用电器行业股票财务指标数据获取':
    st.subheader('//申万家用电器行业股票财务指标数据获取//')
    st.subheader('原始数据（取前100条） =====')
    ss2 = pd.read_excel('上市公司财务与指标数据2013-2017.xlsx')
    st.dataframe(ss2.head(100),use_container_width=True)

    st.subheader('代码 =====')
    st.code(s2,language='python')
    st.subheader('结果 =====')
    r=step2.return_values()
    r
    
if nm=='3.申万家用电器行业股票财务指标数据处理':
    st.subheader('//申万家用电器行业股票财务指标数据处理//')
    st.subheader('原始数据（取前100条）')
    sst3=step2.return_values() 
    st.dataframe(sst3.head(100))

    st.subheader('代码 =====')
    st.code(s3,language='python')
    st.subheader('结果 =====')
    x,code=step3.return_values()
    df=pd.DataFrame(x)
    df['Stkcd']=code
    df
    
if nm=='4.主成分累计贡献率在95%':
    st.subheader('//主成分累计贡献率在95%//')
    st.subheader('原始数据')
    ss4=step3.return_values()
    st.dataframe(pd.DataFrame(ss4[0]))
    st.subheader('代码 =====')
    st.code(s4,language='python')
    st.subheader('结果 =====')
    r=step4.return_values()
    df=pd.DataFrame(r)
    df
    
if nm=='5.家电行业2017年的股票交易数据':
    st.subheader('//家电行业2017年的股票交易数据//')
    st.subheader('原始数据（取前100条）')
    ss5=pd.read_excel('股票交易数据_2017.xlsx') 
    st.dataframe(ss5.head(100))
    
    st.subheader('代码 =====')
    st.code(s5,language='python')
    st.subheader('结果 =====')
    r = step5.return_values()
    df = pd.DataFrame(r)

    df['Trddt'] = pd.to_datetime(df['Trddt'], format='%Y-%m-%d')
    st.dataframe(df)
    
    st.subheader('可视化走势图 =====')
    
    #获取前5只股票的代码
    top5_stocks = df['Stkcd'].unique()[:5]
    #保留Stkcd在top5_stocks中的行
    plot_data = df[df['Stkcd'].isin(top5_stocks)]
    
    #绘图
    plt.figure(figsize=(10, 5))
    for code, group in plot_data.groupby('Stkcd'):
        # 按股票代码分组绘图，x轴为日期，y轴为收盘价
        plt.plot(group['Trddt'], group['Clsprc'], markersize=3, label=str(code))
    
    plt.title('家电行业股票收盘价走势')
    plt.xlabel('交易日期')
    plt.ylabel('收盘价')
    plt.xticks(rotation=45)
    plt.legend(loc='best')
    plt.tight_layout()
    
    # 显示图表
    st.pyplot(plt.gcf())

if nm=='6.家用电器行业交易指数':
    st.subheader('//家用电器行业交易指数//')
    st.subheader('原始数据（取前100条）')
    ss6=step5.return_values()
    st.dataframe(ss6.head(100))
    st.subheader('代码')
    st.code(s6,language='python')
    st.subheader('结果')
    index_val = step6.return_values()  
    df = index_val.reset_index()  # 转换为DataFrame：列名=['Trddt', 0]
    df.columns = ['Trddt', '行业指数']  # 重命名列
    st.dataframe(df)
    
    import matplotlib.dates as mdates

    st.subheader('可视化走势图')
    index_val = step6.return_values()
    df = index_val.reset_index()
    df.columns = ['Trddt', '行业指数']

    df['Trddt'] = pd.to_datetime(df['Trddt'], format='%Y-%m-%d')  
    
    df = df.sort_values('Trddt')
    x = df['Trddt'][:501]
    y = df['行业指数'][:501]
    
    # 绘图
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(x, y, linewidth=2, color='blue', label='指数走势')
    
    # 设置x轴按月显示
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # 显示年份
    
    # 其他样式
    ax.set_xlabel('交易日期')
    ax.set_ylabel('行业指数')
    ax.set_title('家用电器行业交易指数走势')
    ax.grid(alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    st.pyplot(fig)


if nm=='7.沪深300指数年度涨跌幅':
    st.subheader('//沪深300指数年度涨跌幅//')
    st.subheader('原始数据（取前100条）')
    ss7=pd.read_excel('沪深300指数交易数据表.xlsx')
    st.dataframe(ss7.head(100))
    st.subheader('代码')
    st.code(s7,language='python')
    st.subheader('结果')
    r=step7.return_values()
    df=pd.DataFrame(r)
    df
    
if nm=='8.沪深300指数2016年指数的关键转折点':
    st.subheader('//沪深300指数2016年指数的关键转折点//')
    st.subheader('原始数据（取前100条）')
    ss8=pd.read_excel('沪深300指数交易数据表.xlsx')
    st.dataframe(ss8.head(100))
    st.subheader('代码')
    st.code(s8,language='python')
    st.subheader('结果')
    r = step8.return_values()  
    df = pd.DataFrame(r)
    st.dataframe(df)
    
    # 全量指数数据处理
    A = pd.read_excel('沪深300指数交易数据表.xlsx')
    A['Idxtrd01'] = pd.to_datetime(A['Idxtrd01'])
    rdata = A[(A['Idxtrd01'] >= '2016-01-01') & (A['Idxtrd01'] <= '2016-12-31')].sort_values('Idxtrd01')
    rdata['交易天数'] = range(len(rdata))
    
    st.subheader('可视化走势图')
    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 绘制指数曲线
    ax.plot(rdata['交易天数'], rdata['Idxtrd05'], 'b-', alpha=0.9, label='指数序列', linewidth=1.2)  
    
    # 绘制转折点
    ax.scatter(r.index, r.values, color='red', s=25, edgecolor='black', linewidth=0.8, zorder=5, label='转折点')  
    
    # 坐标轴与标题
    ax.set_xlabel('交易天数')
    ax.set_ylabel('收盘指数')
    ax.set_title('2016年沪深300指数关键转折点')
    ax.legend(loc='upper right', fontsize=10)  
    
    # 网格与边框
    ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    st.pyplot(fig)
    
if nm=='9.沪深300指数2016年平均收盘':
    st.subheader('//沪深300指数2016年平均收盘//')
    st.subheader('原始数据（取前100条）')
    ss9=pd.read_excel('沪深300指数交易数据表.xlsx')
    st.dataframe(ss9.head(100))
    st.subheader('代码')
    st.code(s9,language='python')
    st.subheader('结果')
    r = step9.return_values()
    df=pd.DataFrame(r)
    df
    
    # 获取原始数据+筛选2016年
    A = pd.read_excel('沪深300指数交易数据表.xlsx')
    # 确保日期列格式正确
    A['Idxtrd01'] = pd.to_datetime(A['Idxtrd01'])
    # 筛选2016年数据并按日期排序
    rdata = A[(A['Idxtrd01'] >= '2016-01-01') & (A['Idxtrd01'] <= '2016-12-31')].sort_values('Idxtrd01')
    
    # 提取数据
    x10, x20, x30, x60 = r
    
    st.subheader('可视化走势图')
    # 绘图
    plt.rcParams['font.sans-serif'] = 'Simhei'
    plt.figure(figsize=(12, 8))
    
    # 绘制沪深300指数
    plt.plot(rdata['Idxtrd01'], rdata['Idxtrd05'], 
             label='沪深300收盘指数', 
             linewidth=1.5,
             color='black')
    
    # 绘制均线
    plt.plot(rdata['Idxtrd01'], x10, label='10日移动平均', linewidth=1, color='blue')
    plt.plot(rdata['Idxtrd01'], x20, label='20日移动平均', linewidth=1, color='orange')
    plt.plot(rdata['Idxtrd01'], x30, label='30日移动平均', linewidth=1, color='green')
    plt.plot(rdata['Idxtrd01'], x60, label='60日移动平均', linewidth=1, color='red')
    
    # 标题和标签
    plt.title('2016年沪深300指数移动平均线', fontsize=14)
    plt.ylabel('指数点位', fontsize=12)
    
    # 图例和网格调整
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.2)  # 降低网格透明度
    
    # 日期标签旋转
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    st.pyplot(plt)
    

if nm=='10.沪深300指数2016年收盘指数的现价指标':
    st.subheader('//沪深300指数2016年收盘指数的现价指标//')
    st.subheader('原始数据(取前100条)')
    ss10=pd.read_excel('沪深300指数交易数据表.xlsx')
    st.dataframe(ss10.head(100))
    st.subheader('代码')
    st.code(s10,language='python')
    st.subheader('结果')
    r=step10.return_values()
    df=pd.DataFrame(r)
    df
    


   
   
    
