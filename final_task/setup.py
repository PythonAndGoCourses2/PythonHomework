from setuptools import setup, find_packages

setup(
    name='pycalc',
    version='0.2',
    packages=find_packages(),
    description='Pure-python command-line calculator.',
    author='Petrovsky Denis',
    author_email='vertuss111@gmail.com',
    scripts=["pycalc.py"],
    py_modules=["pycalc", "parser"],
    entry_points={'console_scripts': ['pycalc=pycalc:main']}
)
