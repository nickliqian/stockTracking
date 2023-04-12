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
        self.ts_code_list = {"招商银行": "600036.SH"}
        # self.ts_code_list = {"招商银行": "600036.SH", "贵州茅台": "600519.SH", "中国平安": "601318.SH", "中国银行": "601988.SH"}
        self.ts_name = None
        self.ts_code = None

    # 获取初始化数据
    def get_data(self, ts_code_items):
        self.ts_name = ts_code_items[0]
        self.ts_code = ts_code_items[1]
        # 获取今天的日期
        self.end_date = time.strftime('%Y%m%d', time.localtime(time.time()))
        # 获取股票数据
        self.df = self.pro.daily(ts_code=self.ts_code, start_date=self.start_date, end_date=self.end_date)
        # 获取当日收益率
        self.df['daily_return'] = self.df['close'].pct_change()
        # 获取波动率
        self.df['volatility'] = self.df['daily_return'].rolling(window=20).std() * np.sqrt(20)
        # 判断是否处于指定阈值的震荡区间
        self.df['is_oscillating'] = self.df['volatility'].apply(lambda x: True if x <= 0.08 else False)

    # 绘制收盘价曲线
    def plot_close(self):
        self.df['close'].plot(figsize=(12, 6))
        plt.title('{} Stock Price'.format(self.ts_name))
        plt.ylabel('Price (CNY)')
        plt.xlabel('Date')
        plt.show()

    # 绘制波动率曲线
    def plot_volatility(self):
        self.df['volatility'].plot(figsize=(12, 6))
        plt.title('{} Stock Volatility'.format(self.ts_name))
        plt.ylabel('Volatility')
        plt.xlabel('Date')
        plt.show()

    # 查找收盘价的局部最小值并绘制图像
    def plot_local_min(self, distance=20):
        # 查找收盘价的局部最小值
        local_min = find_peaks(-self.df['close'], distance=distance)[0]
        # 绘制收盘价曲线
        self.df['close'].plot(figsize=(12, 6))
        # 绘制局部最小值
        plt.plot(local_min, self.df['close'][local_min], 'ro')
        plt.title('{} Stock Price'.format(self.ts_name))
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
        local_min = find_peaks(-self.df['close'], distance=100)[0]
        ax1.plot(local_min, self.df['close'][local_min], 'ro')

        ax1.set_ylabel('Close Price')
        ax2.set_ylabel('Volatility')
        plt.title('Stock Price and Volatility of {}'.format(self.ts_name))
        plt.show()

    def run_task(self, plot_close=False,
                 plot_volatility=False,
                 plot_local_min=False, distance=20,
                 plot_close_volatility=False):
        for ts_code_items in self.ts_code_list.items():
            self.get_data(ts_code_items)
            # 画图
            if plot_close:
                self.plot_close()
            if plot_volatility:
                self.plot_volatility()
            if plot_local_min:
                self.plot_local_min(distance=20)
            if plot_close_volatility:
                self.plot_close_volatility()
        return self.df


if __name__ == '__main__':
    stk = STK()
    stk.run_task(plot_close=False,
                 plot_volatility=False,
                 plot_local_min=True, distance=20,
                 plot_close_volatility=False)






