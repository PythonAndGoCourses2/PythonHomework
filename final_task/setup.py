from setuptools import setup, find_packages


setup(name='pycalc',
      version='0.1',
      description='A command-line utility which receives mathematical '
                  'expression string as an argument and prints evaluated result.',
      url='https://github.com/BSroad/PythonHomework',
      author='Mariya Polyakova',
      author_email='polyakova.maria.bs@gmail.com',
      license='free',
      packages=find_packages(),
      zip_safe=False,
      entry_points={
        'console_scripts': ['pycalc=pycalc:main'], },)
