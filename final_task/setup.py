from setuptools import setup , find_packages

setup(
    name="pycalc",
    version="0.0.4",
    author="Aliaksei Milto",
    author_email="alexeymilto@gmail.com",
    description="Pure-python command line calculator",
    long_description="""This is a pure-python command line calculator. 

Syntax: pycalc <EXPRESSION>

Operations 
+, -, *, /, //, %, ^, >, <, >=, <=, =, !=, (), sin(), cos(), tan(), atan(), asin(), acos(), degrees(), exp(), sqrt()

I want to thank my uncle for explaining me the algorithm of solving this task.
And my parents who believed in me.""",
    long_description_content_type="text/markdown",
    url="",
    packages=["calculator"],
	entry_points={
        "console_scripts": ["pycalc=calculator.pycalc3:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	
)