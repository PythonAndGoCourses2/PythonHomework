import setuptools

setuptools.setup(
    name="pycalc",
    version="0.1",
    author="Lizaveta_Savanovich",
    author_email="liza.savanovich@mail.ru",
    description="Command-line calculator",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['pycalc = pycalc:main']},
    py_modules=['pycalc'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
