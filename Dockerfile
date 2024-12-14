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

# Install dependencies first (this layer will be cached if dependencies don't change)
RUN python -m venv /venv/cpython && \
    . /venv/cpython/bin/activate && \
    pip install --upgrade pip wheel setuptools

# Copy the rest of the code
COPY . .

# Install the project
RUN . /venv/cpython/bin/activate && pip install -e .

FROM pypy:3.10-slim AS pypy-base
WORKDIR /app

# Copy only dependency files first
COPY pyproject.toml setup.py ./

# Install build essentials for PyPy
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create PyPy virtual environment
RUN pypy3 -m venv /venv/pypy && \
    . /venv/pypy/bin/activate && \
    pip install --upgrade pip wheel setuptools

# Copy the rest of the code
COPY . .

# Install the project and dependencies
RUN . /venv/pypy/bin/activate && \
    pip install psutil memory-profiler matplotlib pandas seaborn && \
    pip install -e .

# Final image combining both environments
FROM pypy:3.10-slim AS final-image
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environments and code
COPY --from=cpython-base /venv/cpython /venv/cpython
COPY --from=cpython-base /app /app
COPY --from=cpython-base /usr/local/bin/python /usr/local/bin/python3.11
RUN ln -s /usr/local/bin/python3.11 /usr/local/bin/python

# Copy PyPy virtual environment
COPY --from=pypy-base /venv/pypy /venv/pypy

# Debug virtual environment contents
RUN echo "=== Final image: CPython venv contents ===" && \
    ls -la /venv/cpython/bin && \
    echo "=== Final image: PyPy venv contents ===" && \
    ls -la /venv/pypy/bin && \
    echo "=== Final image: System executables ===" && \
    ls -la /usr/local/bin/python* /usr/local/bin/pypy* 2>/dev/null || true && \
    echo "=== Final image: PyPy libraries ===" && \
    ls -la /usr/local/lib/pypy* 2>/dev/null || true

# Set up environment variables
ENV PATH="/venv/pypy/bin:/venv/cpython/bin:/usr/local/bin:$PATH" \
    PYTHONPATH=/app \
    LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"

# Copy the entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
