from setuptools import setup, find_packages


setup(name='pycalc',
      version='1.0',
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
      py_modules=['pycalc', 'tool', 'config', 'validation'],
      zip_safe=False,
      )
