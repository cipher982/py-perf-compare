# src package initialization
# This file makes the src directory a proper Python package

import importlib.util


def import_cython_module(module_name):
    try:
        # Try importing the Cython module
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    except ImportError:
        pass
    return None


# Try importing Cython modules
cython_cpu_test = import_cython_module("src.cython_cpu_test")
cython_memory_test = import_cython_module("src.cython_memory_test")
cython_mixed_test = import_cython_module("src.cython_mixed_test")
