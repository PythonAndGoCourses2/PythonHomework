from setuptools import setup, find_packages

setup(
    name='pycalc',
    version='1.0',
    packages=find_packages(),
    description='Pure-python command-line calculator.',
    entry_points={'console_script': ['pycalc=pycalc:main']},
    platforms='any',
)
