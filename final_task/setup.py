from setuptools import setup, find_packages

setup(
    name='pycalc',
    version='1.0',
    author='Mikhail Sauchuk',
    author_email='mishasavchuk@gmail.com',
    packages=find_packages(),
    entry_points={'console_scripts': ['pycalc = pycalc:main']},
    description='Pure-python command-line calculator.',
    platforms='any',
    py_modules=['pycalc']
)


from setuptools import setup

setup(
   # name='pycalc',
   # version='1.0',
   # description='Pure-python command-line calculator.',
   # author='Dubovik Pavel',
   # author_email='geometryk@gmail.com',
   # py_modules=['pycalc'],
   entry_points = {'console_scripts': ['pycalc=pycalc:byild_parser',],},
   # platforms='any',
)