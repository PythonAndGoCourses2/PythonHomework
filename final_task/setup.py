from setuptools import setup, find_packages

setup(
    name="pycalc",
    version="1.0.0",
    description="Pure-python command calculator",
    packages=["src"],
    entry_points={
        "console_scripts": ["pycalc=src.pycalc:main"]}
)
