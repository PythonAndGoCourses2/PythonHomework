from setuptools import setup

setup(name='calculator',
      version='1.0',
      description='calculator python',
      url='pashakorsh.com',
      author='pashakorsh',
      author_email='pashakorsh@gmail.com',
      license='MIT',
      packages=['calculator'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      entry_points = {
          'console_scripts': [
              'calc = calculator.cli:main'
          ]
      }
)
