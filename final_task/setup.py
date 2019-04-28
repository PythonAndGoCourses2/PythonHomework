from setuptools import setup

setup(
    name='pycalc',
    version='1.0',
    packages=["calculator"],
    description='Pure-python command-line calculator.',
    entry_points={
        "console_scripts": ["pycalc=calculator.pycalc:main"]
    },
    platforms='any',
)
