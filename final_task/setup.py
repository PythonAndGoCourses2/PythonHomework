from setuptools import setup

setup(name='pycalc', version='1.0', author='Molchanov Nikita', author_email='molchanovnik7@gmail.com',
      entry_points={'console_scripts': ['pycalc = pycalc:start_calc']},
      platforms='any', py_modules=['pycalc'],)
