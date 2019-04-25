from setuptools import setup, find_packages

setup(
    name='pycalc',
    version='1.0',
    author='Mikhail Sauchuk',
    author_email='mishasavchuk@gmail.com',
    packages=find_packages(),
    entry_points={'console_scripts': ['pycalc = calc:main']},
    description='Pure-python command-line calculator.',
    platforms='any',
    py_modules=['pycalc']
)

