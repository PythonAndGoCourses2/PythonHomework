from setuptools import setup, find_packages

setup(
    name='pycalc',
    version='2.0',
    packages=find_packages(),
    description='Pure-python command-line calculator.',
    author='Petrovsky Denis',
    author_email='vertuss111@gmail.com',
    py_modules=["pycalc", "core", "check", "constants"],
    entry_points={'console_scripts': ['pycalc=pycalc:main']}
)
