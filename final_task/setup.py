#!/usr/bin/env python3


from setuptools import setup


setup(name="pycalc",
      version="1.0",
      description="Pure-python command-line calculator",
      url="https://github.com/WFLM/PythonHomework",
      author="Yury Kuznetsov",
      author_email="yurykuznetsov@protonmail.com",
      scripts=["pycalc.py"],
      entry_points={"console_scripts": ['pycalc=pycalc:main']}
      )
