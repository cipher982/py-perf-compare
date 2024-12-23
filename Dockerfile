# Base image with both Python implementations
FROM python:3.11-slim
WORKDIR /app

# Install PyPy
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    pypy3 \
    && rm -rf /var/lib/apt/lists/*

# Set up virtual environments (but don't install project dependencies yet)
RUN python -m venv /venv/cpython && \
    pypy3 -m venv /venv/pypy

# Update pip in both environments
RUN . /venv/cpython/bin/activate && pip install --upgrade pip wheel setuptools && \
    . /venv/pypy/bin/activate && pip install --upgrade pip wheel setuptools

# Set up environment variables
ENV PATH="/venv/pypy/bin:/venv/cpython/bin:$PATH"

# Set up entrypoint
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
