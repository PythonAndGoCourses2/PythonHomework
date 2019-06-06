from setuptools import setup, find_packages

setup(
    name='pycalc',
    version='1.0',
    author='Antos Shakhbazau',
    author_email='Shakhbazau@gmail.com',
    packages=find_packages(),
    description='Pure-python command line calculator.',
    py_modules=['pycalc'],
    entry_points={'console_scripts': ['pycalc=pycalc:main', ], },
)
