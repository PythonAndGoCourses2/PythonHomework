
from setuptools import setup, find_packages
setup(
    name="pycalc",
    version='0.1',
    author='Oleg Liasota',
    author_email='Liasota1023@gmail.com',
    packages=find_packages(),
    py_modules=['calc'],
    entry_points={
        'console_scripts': [
            'pycalc=calculator.calc:main',
        ],
    },
    platforms='any',
)
