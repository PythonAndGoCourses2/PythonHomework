from setuptools import setup, find_packages

setup(
    name='pycalc',
    version='1.0',
    packages=find_packages(),
    description='Pure-python command-line calculator.',
    py_modules=["pycalc", "tests"],
    entry_points={'console_scripts': ['pycalc=pycalc:main']}
    )
