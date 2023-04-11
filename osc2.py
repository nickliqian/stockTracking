import tushare as ts
import pandas as pd
import numpy as np
import os
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import time


class STK(object):
    def __init__(self):
        self.ts = ts
        self.ts.set_token(os.getenv("TS_PRO_TOKEN"))
        self.pro = self.ts.pro_api()
        self.df = None
        self.start_date = '2020-01-01'
        self.end_date = None
        self.ts_code_list = ['600036.SH']

    # 获取初始化数据
    def get_data(self, ts_code):
        # 获取今天的日期
        self.end_date = time.strftime('%Y%m%d', time.localtime(time.time()))
        # 获取股票数据
        self.df = self.pro.daily(ts_code=ts_code, start_date=self.start_date, end_date=self.end_date)
        # 获取当日收益率
        self.df['daily_return'] = self.df['close'].pct_change()
        # 获取波动率
        self.df['volatility'] = self.df['daily_return'].rolling(window=20).std() * np.sqrt(20)
        # 判断是否处于指定阈值的震荡区间
        self.df['is_oscillating'] = self.df['volatility'].apply(lambda x: True if x <= 0.08 else False)

    # 绘制收盘价曲线
    def plot_close(self):
        self.df['close'].plot(figsize=(12, 6))
        plt.title('CMB Stock Price')
        plt.ylabel('Price (CNY)')
        plt.xlabel('Date')
        plt.show()

    # 绘制波动率曲线
    def plot_volatility(self):
        self.df['volatility'].plot(figsize=(12, 6))
        plt.title('CMB Stock Volatility')
        plt.ylabel('Volatility')
        plt.xlabel('Date')
        plt.show()

    # 查找收盘价的局部最小值并绘制图像
    def plot_local_min(self):
        # 查找收盘价的局部最小值
        local_min = find_peaks(-self.df['close'])[0]
        # 绘制收盘价曲线
        self.df['close'].plot(figsize=(12, 6))
        # 绘制局部最小值
        plt.plot(local_min, self.df['close'][local_min], 'ro')
        plt.title('CMB Stock Price')
        plt.ylabel('Price (CNY)')
        plt.xlabel('Date')
        plt.show()

    # 把收盘价曲线和波动率曲线画在一起
    def plot_close_volatility(self):
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.plot(self.df['trade_date'], self.df['close'], color='b')
        ax2.plot(self.df['trade_date'], self.df['volatility'], color='r')

        # 查找收盘价的局部最小值
        # local_min = find_peaks(-self.df['close'])[0]
        # ax1.plot(local_min, self.df['close'][local_min], 'ro')
        # 查找收盘价的局部最小值，但要求周期大于等于20天
        local_min = find_peaks(-self.df['close'], distance=20)[0]
        ax1.plot(local_min, self.df['close'][local_min], 'ro')

        ax1.set_ylabel('Close Price')
        ax2.set_ylabel('Volatility')
        plt.title('Stock Price and Volatility of China Merchants Bank')
        plt.show()

    def run_task(self):
        for ts_code in self.ts_code_list:
            self.get_data(ts_code)
            # 画图
            self.plot_close()
            self.plot_volatility()
            self.plot_local_min()
            self.plot_close_volatility()
        return self.df


if __name__ == '__main__':
    stk = STK()
    stk.run_task()