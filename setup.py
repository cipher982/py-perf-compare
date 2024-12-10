from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

# Define Cython extensions with NumPy include path
extensions = [
    Extension(
        "cython_cpu_test", 
        ["src/cython_cpu_test.pyx"],
        include_dirs=[numpy.get_include()]
    ),
    Extension(
        "cython_memory_test", 
        ["src/cython_memory_test.pyx"],
        include_dirs=[numpy.get_include()]
    ),
    Extension(
        "cython_mixed_test", 
        ["src/cython_mixed_test.pyx"],
        include_dirs=[numpy.get_include()]
    )
]

setup(
    name='python-performance-tests',
    ext_modules=cythonize(
        extensions, 
        compiler_directives={'language_level': "3"}
    ),
    include_dirs=[numpy.get_include()]
)
