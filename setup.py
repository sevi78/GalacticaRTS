from setuptools import setup
from Cython.Build import cythonize

setup(
        name='galactica app',
        ext_modules=cythonize("main.pyx")
        ,
        )
