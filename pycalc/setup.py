import setuptools

setuptools.setup(
    name="pycalc",
    version="0.1",
    author="Lizaveta_Savanovich",
    author_email="liza.savanovich@mail.ru",
    description="Command-line calculator",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['pycalc = pycalc:main']},
    py_modules=['pycalc'],
)
