from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='pycalc',
    version='0.1.0',
    description='A pure-python command-line calculator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/siarhiejkresik/PythonHomework',
    packages=find_packages(),
    author='Siarhiej Kresik',
    author_email='siarhiej.kresik@gmail.com',
    keywords='calculator calc cli',
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "pycalc=pycalc.__main__:main",
        ]
    },
)
