import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pycalc',
    version='1.0',

    author="Maxim Tsyba",
    author_email="maksimtsuba@gmail.com",
    description="Calculator for EPAM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/javatechy/dokr",
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['pycalc = pycalc:main']},
    py_modules=["pycalc"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
