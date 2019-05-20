from setuptools import setup

setup(
    name="pycalc",
    version="0.0.1",
    author="Pavel Stashchenko",
    author_email="stashchen@gmail.com",
    packages=find_packages(),
    description='Pure-python command-line calculator.',
    py_modules=["calc", "test_calc"],
    entry_points={'console_scripts': ['pycalc=calc:main']}
)
