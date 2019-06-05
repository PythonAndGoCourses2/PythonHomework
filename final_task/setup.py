from setuptools import setup

setup(
    name='pycalc',
    version='1.0',
    description='Pure-python command-line calculator.',
    url='',
    author='Layeuskaya Alina',
    author_email='cool.girl.alina@mail.ru',
    py_modules=['pycalc', 'config', 'pycalc_proc'],
    entry_points={'console_scripts': ['pycalc=pycalc:main', ], },
)
