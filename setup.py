from setuptools import setup, find_packages

setup(
   name='pycalc',
   version='1.0',
   packages=find_packages(),
   description='Pure-python command-line calculator.',
   author='Aliaksandr Serada',
   author_email='alsereda1992.com',
   py_modules=['pycalc'],
   entry_points={'console_scripts': ['pycalc = mycalc.pycalc:main', ], },
   platforms='any',
)