from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = 'pycalc',
    version = '0.1',
    author = 'Mad',
    long_description = long_description,
    packages = find_packages(),
    entry_points={ 
        'console_scripts': [
            'pycalc=__init__:main',
        ],
    }
)