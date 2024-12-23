# Multi-stage build for different Python implementations
FROM python:3.11-slim AS cpython-base
WORKDIR /app

# Copy only dependency files first
COPY pyproject.toml setup.py ./

# Install build dependencies for CPython
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy source files needed for Cython compilation
COPY src/ src/

# Install dependencies and build Cython modules
RUN python -m venv /venv/cpython && \
    . /venv/cpython/bin/activate && \
    pip install --upgrade pip wheel setuptools && \
    pip install -e . && \
    python setup.py build_ext --inplace

FROM pypy:3.10-slim AS pypy-base
WORKDIR /app

# Copy only dependency files first
COPY pyproject.toml setup.py ./

# Copy source files needed for Cython compilation
COPY src/ src/

# Install build essentials for PyPy
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create PyPy virtual environment and build Cython modules
RUN pypy3 -m venv /venv/pypy && \
    . /venv/pypy/bin/activate && \
    pip install --upgrade pip wheel setuptools && \
    pip install psutil memory-profiler matplotlib pandas seaborn && \
    pip install -e . && \
    python setup.py build_ext --inplace

# Final image combining both environments
FROM pypy:3.10-slim AS final-image
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy Python environments and binaries
COPY --from=cpython-base /venv/cpython /venv/cpython
COPY --from=cpython-base /app /app
COPY --from=cpython-base /usr/local/bin/python /usr/local/bin/python3.11
COPY --from=cpython-base /usr/local/lib/libpython3.11.so* /usr/local/lib/
RUN ln -s /usr/local/bin/python3.11 /usr/local/bin/python

# Copy PyPy environment
COPY --from=pypy-base /venv/pypy /venv/pypy

# Debug virtual environment contents
RUN echo "=== Final image: CPython venv contents ===" && \
    ls -la /venv/cpython/bin && \
    echo "=== Final image: PyPy venv contents ===" && \
    ls -la /venv/pypy/bin

# Set up environment variables
ENV PATH="/venv/pypy/bin:/venv/cpython/bin:/usr/local/bin:$PATH" \
    PYTHONPATH=/app \
    LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"

# Set up entrypoint
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
