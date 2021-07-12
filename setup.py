# -*- coding: utf-8 -*- 
# @Time : 2/20/21 3:03 PM 
# @Author : mxt
# @File : setup.py
import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GITCodeAnalysis",
    version="1.0.0",
    author="Maoxinteng",
    author_email="1214403402@qq.com",
    description="Git Code Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mxtadmin/code_analysis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)
