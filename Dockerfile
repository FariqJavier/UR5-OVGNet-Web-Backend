FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsndfile1 ffmpeg curl git && \
    rm -rf /var/lib/apt/lists/*

# Install poetry for dependency management
RUN pip install --no-cache-dir poetry

# Copy project files
COPY pyproject.toml poetry.lock /app/

# Install Python dependencies
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

# Copy application files
COPY . /app

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]