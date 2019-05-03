from setuptools import setup, find_packages

setup(
   name='pycalc',
   version='2.0',
   packages=find_packages(),
   description='calculator.',
   author='Honery',
   author_email='^_--',
   py_modules=['pycalc'],
   entry_points={'console_scripts': ['pycalc = pycalc.pycalc:start', ], },
   platforms='any',
)