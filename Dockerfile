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

# Launch FastAPI with Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]