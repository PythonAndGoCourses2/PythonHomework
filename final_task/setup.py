from setuptools import setup, find_packages
setup(
	name="Pycalc",
	version="1.0",
	description="Pure-Python command line calculator. \n"
				"Python training program kindly supported by EPAM Systems, Minsk.",
	author="Antos Shakhbazau",
	author_email="Shakhbazau@gmail.com",
	python_requires='>=3.6',
	packages=find_packages(),
	entry_points={
		'console_scripts': [
			'pycalc = pycalc.launcher:main',
		],
	}
)
