from setuptools import setup

setup(name='pycalc',
      version='0.1',
      author_email='andrey-truhan@tut.by',
      description='Alpha version pure-python command-line calculator',
      author='Andrei Trukhan',
      license='free',
      packages=['pycalc'],
      zip_safe=False,
      entry_points={
            "console_scripts": ["pycalc=pycalc.start:main"]
      },
      )
