from setuptools import setup, find_packages
setup(
    name="pycalc",
    packages=find_packages(),
    version = "1.0.0",
    entry_points = {
        'console_scripts':['pycalc = src.pycalc:main']
    }
)