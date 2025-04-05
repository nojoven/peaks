# Stage 1: Builder (install dependencies and create virtual environment)
FROM python:3.11-slim-bookworm AS builder

# Set working directory for build stage
WORKDIR /build

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install system dependencies (required for psycopg2, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and activate Python virtual environment
RUN python -m venv /opt/venv

# Set VIRTUAL_ENV and update PATH (this is crucial)
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Python dependencies
RUN python -m pip install --no-cache-dir -r requirements.txt

# ---

# Stage 2: Runtime (lightweight production image)
FROM python:3.11-slim-bookworm

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Set VIRTUAL_ENV and update PATH in runtime
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy entire project (mirrors local structure)
COPY . /peaks
WORKDIR /peaks  # All commands will run from /peaks

# Set Python path (optional, helps with imports)
ENV PYTHONPATH=/peaks

# Expose FastAPI port
EXPOSE 8000

# Copy MkDocs documentation
COPY docs/site /app/docs/site

# Copy the entrypoint script from the root (peaks/entrypoint.sh)
COPY entrypoint.sh /peaks/entrypoint.sh
# Ensure the entrypoint script is executable
RUN chmod +x /peaks/entrypoint.sh

# Launch FastAPI with Uvicorn via the entrypoint script
CMD ["sh", "/peaks/entrypoint.sh"]