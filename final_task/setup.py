from setuptools import setup, find_packages

setup(
    name='pycalc',
    version='1.0',
    author='Pavel Karshakevich',
    author_email='pashakorsh@gmail.com',
    packages=find_packages(),
    entry_points={'console_scripts': ['pycalc = pycalc.cli:main']},
    description='Pure-python command-line calculator.',
    py_modules=['pycalc']
)
