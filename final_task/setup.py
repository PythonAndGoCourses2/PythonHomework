from setuptools import setup, find_packages

setup(name='pycalc',
      version='0.1',
      description='Alpha version pure-python command-line calculator',
      url='https://github.com/Vaires/PythonHomework',
      author='Volha Halynskaya',
      author_email='volha.halynskaya@gmail.com',
      entry_points={'console_scripts': ['pycalc = pycalc:main']},
      license='free',
      packages=find_packages(),
      py_modules=["pycalc"]
      )
