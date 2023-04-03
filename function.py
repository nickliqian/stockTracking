import tushare as ts
import os
import time

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