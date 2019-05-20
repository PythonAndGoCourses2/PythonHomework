from setuptools import setup

setup(
    name="pycalc",
    version="0.0.1",
    author="Pavel Stashchenko",
    author_email="stashchen@gmail.com",
    description="Pure-python command line calculator",
    entry_points={
        "console_scripts": ["pycalc=Calculator.calc:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)