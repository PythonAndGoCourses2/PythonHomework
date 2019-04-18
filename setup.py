from setuptools import setup

setup(
   name='pycalc',
   version='1.0',
   description='Pure-python command-line calculator.',
   author='Dubovik Pavel',
   author_email='geometryk@gmail.com',
   py_modules=["pycalc"],			
   entry_points = {'console_scripts': ['pycalc=pycalc:main',],},
)