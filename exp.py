import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


ts.set_token(os.getenv("TS_PRO_TOKEN"))

# 获取招商银行过去三年的股票数据
start_date = '2018-04-03'
end_date = '2021-04-03'
df = ts.get_k_data('600036', start=start_date, end=end_date)

# 计算每日收益率和波动率
df['daily_return'] = df['close'].pct_change()
df['volatility'] = df['daily_return'].rolling(window=20).std() * np.sqrt(20)

# 标记震荡周期和非震荡周期
df['is_oscillating'] = df['volatility'].apply(lambda x: True if x <= 0.08 else False)

# 确定震荡周期和非震荡周期的开始和结束位置
oscillating_periods = df.index[df['is_oscillating'] != df['is_oscillating'].shift(1)]
non_oscillating_periods = df.index[df['is_oscillating'] != df['is_oscillating'].shift(-1)]

# 标记震荡周期和非震荡周期的范围
for start, end in zip(oscillating_periods, non_oscillating_periods):
    plt.axvspan(df['date'][start], df['date'][end], color='gray', alpha=0.2)

# 绘制股票收盘价和波动率曲线
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(df['date'], df['close'], color='b')
ax2.plot(df['date'], df['volatility'], color='r')
ax1.set_ylabel('Close Price')
ax2.set_ylabel('Volatility')
plt.title('Stock Price and Volatility of China Merchants Bank')
plt.show()
