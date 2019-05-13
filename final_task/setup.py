import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='pycalc',
    version='1.0',
    description='Pure-python command-line calculator.',
    long_description=read('README.md'),
    packages=find_packages(),
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "pycalc=calculator.pycalc:main",
        ]
    },
    platforms='any',
)
