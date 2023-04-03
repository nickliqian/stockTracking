import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 设置tushare pro的token，用于获取数据
ts.set_token(os.getenv("TS_PRO_TOKEN"))

# 初始化pro接口
pro = ts.pro_api()

# 获取招商银行过去三年的日线数据
df = pro.daily(ts_code='600036.SH', start_date='20200101', end_date='20211231')

# 转换日期格式
df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')

# 计算每日的波动率
df['daily_return'] = df['close'].pct_change()
df['volatility'] = df['daily_return'].rolling(window=20).std() * np.sqrt(20)

# 通过波动率确定震荡周期
df['is_oscillating'] = df['volatility'].apply(lambda x: True if x <= 0.08 else False)

# 绘制波动率和震荡周期图表
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(df['trade_date'], df['volatility'], color='blue', label='Volatility')
ax.set_ylabel('Volatility')
ax.set_xlabel('Date')
ax2 = ax.twinx()
ax2.plot(df['trade_date'], df['is_oscillating'], color='red', label='Is Oscillating')
ax2.set_yticks([0, 1])
ax2.set_yticklabels(['False', 'True'])
ax2.set_ylabel('Is Oscillating')
plt.title('招商银行波动率和震荡周期图表')
plt.show()

# 计算震荡周期的平均长度
oscillating_periods = df[df['is_oscillating'] == True]['is_oscillating']

# 取oscillating_periods第一个元素
oscillating_periods_0_ele = np.concatenate(([oscillating_periods.index[0]], oscillating_periods.index))

oscillating_periods = np.diff(np.where(np.concatenate((oscillating_periods_0_ele,
                                                        np.diff(oscillating_periods),
                                                        [oscillating_periods[-1]])))[0])[::2]
average_oscillating_period = np.mean(oscillating_periods)

# 输出结果
print('招商银行股票波动率和震荡周期分析结果：')
print('平均震荡周期长度：', average_oscillating_period)
