from setuptools import setup, find_packages


setup(name='pycalc',
      version='0,1',
      description='Pure python calculator',
      url='http://github.com/AndreyFesko/PythonHomework',
      author='Andrey Fesko',
      author_email='AndreyFesko@gmail.com',
      keywords='python calculator',
      packages=find_packages(),
      entry_points={
              'console_scripts': [
                  'pycalc = pycalc:start',
              ],
      },
      zip_safe=False,
      )
