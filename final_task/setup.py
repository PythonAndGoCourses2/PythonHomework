from setuptools import setup, find_packages

setup(
    name='Calculate',
    version='1.0',
    packages=find_packages(),
    description='Pure-python command-line calculator.',
    author='Petrovsky Denis',
    author_email='vertuss111@gmail.com',
    entry_points={'console_scripts':['pycalc=pycalc:main']}
)
