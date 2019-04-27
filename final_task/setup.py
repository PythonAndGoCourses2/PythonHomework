from setuptools import setup, find_packages
from os import path

setup(
    name = 'pycalc',
    version = '0.1',
    packages = [],
    entry_points={ 
        'console_scripts': [
            'pycalc=__init__:main',
        ],
    }
)