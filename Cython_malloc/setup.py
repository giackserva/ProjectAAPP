from distutils.core import setup, Extension
from Cython.Build import cythonize

setup(
	name = 'Cython SkipList implementation',
        ext_modules = cythonize("*.pyx"),
	# ext_modules = cythonize("SkipList_old.pyx"),
)
