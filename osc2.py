import tushare as ts
import pandas as pd
import numpy as np
import os
from scipy.signal import find_peaks


# 获取招商银行过去三年的股票数据
pro = ts.pro_api(os.getenv("TS_PRO_TOKEN"))
df = pro.daily(ts_code='600036.SH', start_date='20180101')

# 计算每日收益率
df['daily_return'] = df['close'].pct_change()

# 计算波动率
df['volatility'] = df['daily_return'].rolling(window=20).std() * np.sqrt(20)

# 判断是否处于震荡市
df['is_oscillating'] = df['volatility'].apply(lambda x: True if x <= 0.08 else False)

# 计算震荡周期
oscillating_periods = np.where(df['is_oscillating'])[0]
if oscillating_periods.size > 0:
    oscillating_periods = np.split(oscillating_periods, np.where(np.diff(oscillating_periods) != 1)[0] + 1)
    oscillating_periods = [periods for periods in oscillating_periods if len(periods) >= 20]
    if oscillating_periods:
        oscillating_periods_lengths = [len(periods) for periods in oscillating_periods]
        avg_oscillating_period = sum(oscillating_periods_lengths) / len(oscillating_periods_lengths)
        print(f"招商银行股票震荡周期的平均长度为{avg_oscillating_period:.2f}个交易日")
    else:
        print("招商银行股票在过去三年内没有出现过震荡周期")
else:
    print("招商银行股票在过去三年内没有出现过震荡周期")


import matplotlib.pyplot as plt

# 绘制收盘价曲线
df['close'].plot(figsize=(12,6))
plt.title('CMB Stock Price')
plt.ylabel('Price (CNY)')
plt.xlabel('Date')
plt.show()

# 绘制波动率曲线
df['volatility'].plot(figsize=(12,6))
plt.title('CMB Stock Volatility')
plt.ylabel('Volatility')
plt.xlabel('Date')
plt.show()

# 绘制震荡区间
oscillating_periods = df[df['is_oscillating'] == True].index
for i in range(0, len(oscillating_periods), 2):
    plt.axvspan(oscillating_periods[i], oscillating_periods[i+1], color='grey', alpha=0.2)
plt.title('CMB Stock Oscillating Periods')
plt.ylabel('Price (CNY)')
plt.xlabel('Date')
plt.show()

# 绘制波动率曲线
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df['trade_date'], df['volatility'], color='blue')
ax.set_title('Volatility of CMB Stock (2018-2021)', fontsize=16)
ax.set_xlabel('Date', fontsize=14)
ax.set_ylabel('Volatility', fontsize=14)

# 查找波谷点
peaks, _ = find_peaks(-df['volatility'].values, distance=20)
ax.plot(df.iloc[peaks]['trade_date'], df.iloc[peaks]['volatility'], 'rx')

plt.show()
