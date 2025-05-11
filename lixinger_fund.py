# lixinger_fund.py
import requests
import pandas as pd
from config import API_KEY, BASE_URL
import json
import pandas as pd

class LixingerFundAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = BASE_URL
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _request(self, endpoint, payload):
        url = f"{self.base_url}{endpoint}"
        payload["token"] = self.api_key
        response = requests.post(url, json=payload, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_fund_detail(self, fund_codes):
        """
        获取公募基金的基本信息
        :param fund_codes: 基金代码列表，如 ["110011"]
        """
        endpoint = "/fund"
        payload = {
            "fs": fund_codes
        }
        return self._request(endpoint, payload)

    def get_fund_value(self, fund_code, start_date, end_date):
        """
        获取基金净值数据
        :param fund_code: 基金代码字符串，如 "110011"
        :param start_date: 开始日期，如 "2024-01-01"
        :param end_date: 结束日期，如 "2024-05-10"
        """
        endpoint = "/fund/net-value"
        payload = {
            "stockCode": fund_code,
            "startDate": start_date,
            "endDate": end_date
        }
        return self._request(endpoint, payload)

    def fund_detail_to_df(self, detail_json):
        """
        基金基本信息转为DataFrame
        """
        return pd.DataFrame(detail_json["data"])

    def fund_nav_to_df(self, nav_json):
        """
        将基金净值接口的返回结果转换为 DataFrame
        """
        if not nav_json.get("data"):
            print("⚠️ data 字段为空或无数据")
            return pd.DataFrame()

        # 直接用 data 列表构建 DataFrame
        df = pd.DataFrame(nav_json["data"])

        # 处理日期格式
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")  # 按时间升序排列
        df = df.reset_index(drop=True)
        return df
