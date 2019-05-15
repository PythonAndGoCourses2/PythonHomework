from setuptools import setup, find_packages

setup(
    name='pycalc_not_my',
    version='1.0',
    author='Mikhail Sauchuk',
    author_email='mishasavchuk@gmail.com',
    packages=find_packages(),
    entry_points={'console_scripts': ['pycalc = pycalc:main']},
    description='Pure-python command-line calculator.',
    platforms='any',
    py_modules=['pycalc']
)
