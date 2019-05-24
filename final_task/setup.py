from setuptools import setup, find_packages
setup(name='pycalc', version='1.0', packages=find_packages(),
      entry_points={'console_scripts': ['pycalc = src.main:calc']},
      platforms='any', py_modules=['pycalc'],)
