'''
理杏仁开放平台API包安装
'''

import lixinger_openapi as lo
from setuptools import find_packages, setup

# 获取版本号
version = lo.__version__

# 读取README.md内容作为长描述
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='lixinger_openapi',
    version=version,
    description='lixinger openapi',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    author='sheki lyu',
    author_email='lvxueji@gmail.com',
    license='Apache License v2',
    install_requires=[
        "requests>=1.0.0",
        "pandas>=1.0.0",
    ],
    url='https://github.com/ShekiLyu/lixinger-openapi',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',  # 移除对Python 2.7的支持
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',  # 指定最低Python版本要求
)