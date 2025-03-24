# Use an appropriate base image
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install the project into `/app`
WORKDIR /app

# Set environment variables (e.g., set Python to run in unbuffered mode)
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Install system dependencies for building libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy the dependency management files (lock file and pyproject.toml) first
COPY pyproject.toml uv.lock /app/

# Install the application dependencies
RUN uv sync --frozen --no-cache

# Copy your application code and assets into the container
COPY src/ /app/src/
COPY README.md /app/

# Run the loading script in the background when the container starts
CMD ["python", "src/main.py"]