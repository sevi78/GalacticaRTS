from Cython.Build import cythonize
from setuptools import setup

setup(
        name='galactica app',
        ext_modules=cythonize("main.pyx")
        ,
        )
