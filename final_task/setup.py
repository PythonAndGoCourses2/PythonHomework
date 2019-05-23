from setuptools import setup, find_packages

setup(
    name='pycalc',
    description='Calculate string expression, input from command interface',
    url='https://github.com/internetdemonnikc/PythonHomework',
    author='Anton Okulenko',
    author_email='okulenko2017@mail.ru',
    classifiers=[
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    version=None,
    packages=find_packages(),
    entry_points={'console_scripts': ['pycalc=pycalc.pycalc:main']}
)
