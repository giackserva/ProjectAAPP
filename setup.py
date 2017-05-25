from distutils.core import setup
from Cython.Build import cythonize

setup(
	name = 'Cython SkipList implementation',
	ext_modules = cythonize("SkipList.pyx"),
)