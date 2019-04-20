from setuptools import setup, find_packages

setup(name='pycalc', version='1.0', author='Molchanov Nikita', packages=find_packages(),
      author_email='molchanovnik7@gmail.com', entry_points={'console_scripts': ['pycalc = pycalc:create_arg_parser']},
      platforms='any', py_modules=['pycalc'],)
