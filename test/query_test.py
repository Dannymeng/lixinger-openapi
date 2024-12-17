# -*- coding: utf-8 -*-
"""
测试代码

注意：因为token值涉及账户隐私，不能在代码里写，所以请在代码所在目录下创建一个token.cfg文件，并将token值写入。token.cfg文件我已经在git里忽略，不会被上库。
"""

from datetime import datetime
from pprint import pp
import sys
import os
import unittest

import pandas as pd

# 将上级目录添加到系统路径中，以便导入自定义模块
if os.path.abspath("..") not in sys.path:
    sys.path.append(os.path.abspath(".."))
from lixinger_openapi.query import (
    query_json,
    query_dataframe,
)


class DataTest(unittest.TestCase):
    """测试理杏仁开放平台API的数据查询功能"""

    def setUp(self):
        """你可以在这里运行一次set_token，写入token.cfg文件，然后再删除token值，这样有了cfg文件以后都不用set_token了"""
        pass
        # set_token("")

    def test_query_json_company(self):
        """测试查询大陆公司基础信息（JSON格式）"""
        rlt = query_json("cn/company", {"fsTableType": "bank"})
        pp(rlt)
        self.assertIn("code", rlt)
        self.assertEqual("success", rlt["message"])
        self.assertGreater(len(rlt["data"]), 0)
        self.assertIn("000001", [x["stockCode"] for x in rlt["data"]])

    def test_query_df_company(self):
        """测试查询大陆公司基础信息（DataFrame格式）"""
        rlt: dict = query_dataframe("cn/company", {"fsTableType": "bank"})
        pp(rlt)
        self.assertIn("code", rlt)
        self.assertGreater(len(rlt), 0)
        df: pd.DataFrame = rlt["data"]
        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertTrue((df["stockCode"] == "000001").any())

    def test_query_json_index(self):
        """测试查询公司所属指数（以宁德时代为例，必在深圳成指）"""
        rlt = query_json("cn/company/indices", {"stockCode": "300750"})
        pp(rlt)
        self.assertIn("code", rlt)
        self.assertEqual("success", rlt["message"])
        self.assertGreater(len(rlt), 0)
        self.assertEqual("cn", rlt["data"][0]["areaCode"])
        深圳成指 = "399001"
        self.assertTrue(
            any(
                r
                for r in rlt["data"]
                if "stockCode" in r and r["stockCode"] == 深圳成指
            )
        )

    def test_query_json_company_industries(self):
        """测试查询公司所属行业（以宁德时代为例）"""
        rlt = query_json("cn/company/industries", {"stockCode": "300750"})
        pp(rlt)
        self.assertIn("code", rlt)
        self.assertEqual("success", rlt["message"])
        self.assertGreater(len(rlt), 0)
        self.assertEqual("cn", rlt["data"][0]["areaCode"])
        self.assertTrue(
            any(r for r in rlt["data"] if "stockCode" in r and r["stockCode"] == "C03")
        )

    def test_query_json_fundamental(self):
        """测试查询指数基本面数据（以上证50指数为例）"""
        date_to_test = "2024-12-10"
        rlt = query_json(
            "cn/index/fundamental",
            {
                "date": date_to_test,
                "stockCodes": ["000016"],
                "metricsList": ["pe_ttm.y10.mcw.cvpos", "pe_ttm.mcw", "mc"],
            },
        )
        pp(rlt)
        self.assertIn("code", rlt)
        self.assertEqual("success", rlt["message"])
        self.assertGreater(len(rlt["data"]), 0)
        data = rlt["data"][0]
        self.assertEqual(date_to_test, _extract_date(data["date"]))
        self.assertAlmostEqual(10.75, rlt["data"][0]["pe_ttm.mcw"], delta=0.01)

    def test_query_json_index_samples(self):
        """测试查询指数样本（以上证50指数为例）"""
        rlt = query_json(
            "cn/index/constituents", {"date": "2017-09-30", "stockCodes": ["000016"]}
        )
        pp(rlt)
        self.assertIn("code", rlt)
        self.assertEqual("success", rlt["message"])
        self.assertIn("000016", [x["stockCode"] for x in rlt["data"]])

    def test_query_df_us_index(self):
        """测试查询美股指数基本信息"""
        rlt = query_dataframe("us/index", {})
        pp(rlt)
        self.assertIn("code", rlt)
        self.assertEqual("", rlt["msg"])
        df: pd.DataFrame = rlt["data"]
        assert isinstance(df, pd.DataFrame)
        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertGreater(len(df), 0)
        self.assertTrue((df["name"] == "标普500").any())


def _extract_date(datetime_str: str) -> str:
    """从ISO格式的日期时间字符串中提取日期部分"""
    return datetime.fromisoformat(datetime_str).strftime("%Y-%m-%d")


if __name__ == "__main__":
    unittest.main()
