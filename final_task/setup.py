from setuptools import setup, find_packages

setup(
    name="pycalc",
    version="0.0.4",
    author="Aliaksei Milto",
    author_email="alexeymilto@gmail.com",
    description="Pure-python command line calculator",
    packages=["calculator"],
    entry_points={
        "console_scripts": ["pycalc=calculator.pycalc3:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

