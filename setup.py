import numpy
from Cython.Build import cythonize
from setuptools import Extension
from setuptools import setup

# Define Cython extensions
extensions = [
    # Pure implementations (no NumPy dependency)
    Extension(
        "src.pure.cpu_test_cython",
        ["src/pure/cpu_test_cython.pyx"],
        include_dirs=[],
    ),
    Extension(
        "src.pure.memory_test_cython",
        ["src/pure/memory_test_cython.pyx"],
        include_dirs=[],
    ),
    Extension(
        "src.pure.mixed_test_cython",
        ["src/pure/mixed_test_cython.pyx"],
        include_dirs=[],
    ),
    # NumPy implementations
    Extension(
        "src.numpy.cpu_test_cython",
        ["src/numpy/cpu_test_cython.pyx"],
        include_dirs=[numpy.get_include()],
    ),
    Extension(
        "src.numpy.memory_test_cython",
        ["src/numpy/memory_test_cython.pyx"],
        include_dirs=[numpy.get_include()],
    ),
]

setup(
    name="python-performance-tests",
    packages=["src", "src.pure", "src.numpy"],
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            "language_level": "3",
            "boundscheck": False,
            "wraparound": False,
            "nonecheck": False,
        },
    ),
)
