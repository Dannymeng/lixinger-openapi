# main.py
import pandas as pd
import requests



from lixinger_fund import LixingerFundAPI
from config import API_KEY

# 初始化API实例
fund_api = LixingerFundAPI(API_KEY)

fund_nav_json = ""


try:
    fund_nav_json  = fund_api.get_fund_value("165531", "2024-01-01", "2024-05-10")
    print(fund_nav_json)
except requests.exceptions.HTTPError as e:
    print("状态码：", e.response.status_code)
    print("返回内容：", e.response.text)
fund_nav_df = fund_api.fund_nav_to_df(fund_nav_json)

import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'SimHei'      # 设置中文字体为黑体（SimHei）
plt.rcParams['axes.unicode_minus'] = False

if not fund_nav_df.empty:
    plt.figure(figsize=(10, 6))
    plt.plot(fund_nav_df["date"], fund_nav_df["netValue"], label="单位净值", marker='o')
    plt.title("基金净值走势图 - 165531")
    plt.xlabel("日期")
    plt.ylabel("单位净值")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
else:
    print("⚠️ 无数据可绘图。")

def compute_return(df):
    """
    计算基金的日收益率与累计收益率
    """
    df = df.copy()
    df["daily_return"] = df["netValue"].pct_change()         # 日收益率
    df["cumulative_return"] = (1 + df["daily_return"]).cumprod() - 1  # 累计收益率
    return df


fund_nav_df = fund_api.fund_nav_to_df(fund_nav_json)
fund_nav_df = compute_return(fund_nav_df)

print(fund_nav_df[["date", "netValue", "daily_return", "cumulative_return"]].tail())


if not fund_nav_df.empty:
    plt.figure(figsize=(12, 6))

    # 子图 1：单位净值
    plt.subplot(2, 1, 1)
    plt.plot(fund_nav_df["date"], fund_nav_df["netValue"], label="单位净值", color="blue")
    plt.ylabel("单位净值")
    plt.grid(True)
    plt.legend()

    # 子图 2：累计收益率（转为百分比显示）
    plt.subplot(2, 1, 2)
    plt.plot(fund_nav_df["date"], fund_nav_df["cumulative_return"] * 100, label="累计收益率", color="green")
    plt.ylabel("累计收益率（%）")
    plt.xlabel("日期")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()
else:
    print("⚠️ 无数据可绘图。")
