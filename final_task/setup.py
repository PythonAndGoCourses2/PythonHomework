#!/usr/bin/env python3

"""pycalc setup script"""


from setuptools import setup, find_packages


setup(
    name="pycalc",
    version="1.0",
    author="Yury Kuznetsov",
    author_email="yurykuznetsov@protonmail.com",
    description="Pure-python command-line calculator",
    url="https://github.com/WFLM/PythonHomework",
    packages=find_packages(exclude=['tests', 'test*']),
    python_requires=">=3.6.0",
    platforms="any",
    test_suite='tests',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ['pycalc=pycalc.pycalc:main']}
)
