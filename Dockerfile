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
COPY ./app/pyproject.toml ./app/poetry.lock /app/

# Install Python dependencies
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

# Install OpenAI Whisper
RUN pip install openai-whisper

# Install Spacy NLP model
RUN python -m spacy download en_core_web_sm

# Copy application files
COPY ./app /app

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]