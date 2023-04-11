import tushare as ts
import os
import time

"""
# 设计一个股票、基金池，监控价格
# 从tushare pro获取数据，绘制股票走势图
# 设定一些监控指标进行计算，例如：
    一个月内最低点、三个月内最低点、半年内最低点、一年内最低点
    一个月内最高点、三个月内最高点、半年内最高点、一年内最高点
    一个月内涨跌幅、三个月内涨跌幅、半年内涨跌幅、一年内涨跌幅
    局部最低点、局部最高点
# 成交量的变化
# 不同时间段的趋势类型，例如震荡、上升、下降
"""


# 使用time获取今天的日期
today = time.strftime('%Y%m%d', time.localtime(time.time()))


# df = ts.get_hist_data('600519', start='2020-01-01', end=today)
# print(df)


# 设置tushare pro的token，用于获取数据
ts.set_token(os.getenv("TS_PRO_TOKEN"))

# 初始化pro接口
pro = ts.pro_api()

# 获取贵州茅台过去三年的日线数据
df = pro.daily(ts_code='600519.SH', start_date='20180101', end_date=today)

# 找到最低点
lowest_price = df['close'].min()
lowest_date = df.loc[df['close'].idxmin(), 'trade_date']

# 输出结果
print('最低价:', lowest_price)
print('日期:', lowest_date)