from setuptools import setup, find_packages
setup(
    name="pycalc.py",
    version="0.1",
    url="https://github.com/Durnevir/PythonHomework",
    include_package_data=True,
    # package_dir={'': 'src'},
    scripts= ['pycalc.py'],
    packages=find_packages(),
    entry_points={
              'console_scripts': [
                  'pycalc = pycalc:start',
              ],
      },
    py_modules=['pycalc']
)
