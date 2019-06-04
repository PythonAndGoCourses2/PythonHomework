from setuptools import setup, find_packages

setup(
    name='pycalc',
    version='1.0',
    author='Alena Karaliova',
    author_email='koroliovalena90@gmail.com',
    packages=find_packages(),
    entry_points={'console_scripts': ['pycalc.cli:main']},
    description='Pure-python command-line calculator.',
    py_modules=['pycalc', 'calc', 'split', 'operators']
)
