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

# Install the project (this will be quick if only source code changed)
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

# Install dependencies first
RUN pypy3 -m venv /venv/pypy && \
    . /venv/pypy/bin/activate && \
    pip install --upgrade pip wheel setuptools

# Copy the rest of the code
COPY . .

# Install the project and additional dependencies
RUN . /venv/pypy/bin/activate && \
    pip install psutil && \
    pip install -e .

# Final image combining both environments
FROM python:3.11-slim AS final-image
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=cpython-base /venv/cpython /venv/cpython
COPY --from=cpython-base /app /app
COPY --from=pypy-base /venv/pypy /venv/pypy

# Copy the entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
