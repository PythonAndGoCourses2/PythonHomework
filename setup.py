import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="pycalc",
	version="0.0.1",
	author="Alena Karaliova",
	author_email="koroliovalena90@gmail.com",
	description="Pure-python command-line calculator.",
	packages=setuptools.find_packages(),
	entry_points={'console_scripts': 
						['pycalc=pycalc:main']},
	py_modules=['pycalc', 'calc', 'split', 'operators']
)
