"""
理杏仁开放平台API包安装
"""

import importlib.util
from pathlib import Path
from types import ModuleType

from setuptools import find_packages, setup


def get_version() -> str:
    """
    获取 _version.py 文件里的版本号
    """
    version_file: Path = Path(__file__) / "lixinger_openapi" / "_version.py"
    assert version_file is not None, "版本文件不存在"
    spec = importlib.util.spec_from_file_location("_version", version_file)
    if spec is None or spec.loader is None:
        print(f"Warning: Could not load version from {version_file}")
        return ""

    # 使用 importlib.util.module_from_spec 创建一个新的模块对象，并执行
    version_module: ModuleType = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(version_module)
    return version_module.__version__


# 读取README.md内容作为长描述
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lixinger_openapi",
    version=get_version(),
    description="lixinger openapi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    author="sheki lyu",
    author_email="lvxueji@gmail.com",
    license="Apache License v2",
    install_requires=[
        "requests",
        "pandas",
        "numpy",
    ],
    url="https://github.com/ShekiLyu/lixinger-openapi",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",  # 移除对Python 2.7的支持
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",  # 指定最低Python版本要求
)
