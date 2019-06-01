from setuptools import setup

setup(
    name='py_calc',
    version='1.0',
    description='Pure-python command-line calculator.',
    url='',
    author='Layeuskaya Alina',
    author_email='cool.girl.alina@mail.ru',
    py_modules=['py_calc', 'config', 'entry_point'],
    entry_points={'console_scripts': ['entry_point=entry_point:main', ], },
)
